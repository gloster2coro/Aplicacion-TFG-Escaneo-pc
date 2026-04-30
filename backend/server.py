from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import Response
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import uuid
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from optidriver import hardware, optimizer, drivers, restore, ai_assistant, docs

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI(title="Optidriver API", version="1.0.0")
api_router = APIRouter(prefix="/api")

# ---------- Models ----------
class ProfileSelect(BaseModel):
    profile: str  # gaming | oficina | optimo

class OptimizeRequest(BaseModel):
    profile: str
    simulate: bool = True

class DriverUpdateRequest(BaseModel):
    driver_names: List[str]
    simulate: bool = True

class RestorePointRequest(BaseModel):
    description: str
    point_type: str = "MODIFY_SETTINGS"

class AIAnalyzeRequest(BaseModel):
    profile: str
    budget: str = "medio"  # bajo | medio | alto
    session_id: Optional[str] = None

class AIChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    include_hardware: bool = False

# ---------- Root ----------
@api_router.get("/")
async def root():
    return {"app": "Optidriver", "version": "1.0.0", "status": "online"}

# ---------- Hardware ----------
@api_router.get("/hardware/full")
async def hardware_full():
    return hardware.get_full_hardware_report()

@api_router.get("/hardware/metrics")
async def hardware_metrics():
    return hardware.get_realtime_metrics()

# ---------- System ----------
@api_router.get("/system/processes")
async def system_processes():
    return {"processes": optimizer.scan_processes()}

@api_router.get("/system/services")
async def system_services():
    return {"services": optimizer.scan_services()}

@api_router.get("/system/startup")
async def system_startup():
    return {"startup_apps": optimizer.scan_startup_apps()}

# ---------- Optimization ----------
@api_router.post("/optimize/analyze")
async def optimize_analyze(req: ProfileSelect):
    return optimizer.analyze_system(req.profile)

@api_router.post("/optimize/apply")
async def optimize_apply(req: OptimizeRequest):
    # Create automatic restore point before applying
    rp = restore.create_restore_point(
        f"Optidriver - Antes de perfil {req.profile}",
        "MODIFY_SETTINGS"
    )
    rp_doc = {
        "id": str(uuid.uuid4()),
        "description": rp["description"],
        "timestamp": rp["timestamp"],
        "simulated": rp.get("simulated", True),
        "source": "auto_before_optimize",
        "profile": req.profile,
    }
    await db.restore_points.insert_one(rp_doc.copy())

    result = optimizer.apply_optimizations(req.profile, simulate=req.simulate)

    log_doc = {
        "id": str(uuid.uuid4()),
        "profile": req.profile,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "simulated": result["simulated"],
        "processes_affected": result["processes_affected"],
    }
    await db.optimization_logs.insert_one(log_doc.copy())

    # Save selected profile
    await db.profiles.update_one(
        {"_id": "current"},
        {"$set": {"profile": req.profile, "updated_at": datetime.now(timezone.utc).isoformat()}},
        upsert=True,
    )

    return {**result, "auto_restore_point": rp_doc}

@api_router.get("/optimize/logs")
async def optimize_logs():
    logs = await db.optimization_logs.find({}, {"_id": 0}).sort("timestamp", -1).to_list(100)
    return {"logs": logs}

@api_router.get("/optimize/current-profile")
async def current_profile():
    doc = await db.profiles.find_one({"_id": "current"}, {"_id": 0})
    return doc or {"profile": None}

# ---------- Drivers ----------
@api_router.get("/drivers")
async def drivers_list():
    return {"drivers": drivers.list_drivers()}

@api_router.get("/drivers/outdated")
async def drivers_outdated():
    return {"drivers": drivers.get_outdated_drivers()}

@api_router.post("/drivers/update")
async def drivers_update(req: DriverUpdateRequest):
    # Create restore point before driver updates
    rp = restore.create_restore_point(
        f"Optidriver - Antes de actualizar {len(req.driver_names)} drivers",
        "DEVICE_DRIVER_INSTALL"
    )
    rp_doc = {
        "id": str(uuid.uuid4()),
        "description": rp["description"],
        "timestamp": rp["timestamp"],
        "simulated": rp.get("simulated", True),
        "source": "auto_before_driver_update",
    }
    await db.restore_points.insert_one(rp_doc.copy())

    result = drivers.update_drivers(req.driver_names, simulate=req.simulate)

    doc = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "drivers": req.driver_names,
        "successes": result["successes"],
        "failures": result["failures"],
        "simulated": result["simulated"],
    }
    await db.driver_updates.insert_one(doc.copy())
    return {**result, "auto_restore_point": rp_doc}

# ---------- Restore Points ----------
@api_router.post("/restore/create")
async def restore_create(req: RestorePointRequest):
    result = restore.create_restore_point(req.description, req.point_type)
    doc = {
        "id": str(uuid.uuid4()),
        "description": result["description"],
        "point_type": result["point_type"],
        "timestamp": result["timestamp"],
        "simulated": result.get("simulated", True),
        "source": "manual",
        "success": result.get("success", True),
    }
    await db.restore_points.insert_one(doc.copy())
    return {**result, "id": doc["id"]}

@api_router.get("/restore/history")
async def restore_history():
    items = await db.restore_points.find({}, {"_id": 0}).sort("timestamp", -1).to_list(100)
    return {"restore_points": items}

# ---------- AI Assistant ----------
@api_router.post("/ai/analyze")
async def ai_analyze(req: AIAnalyzeRequest):
    try:
        hw = hardware.get_full_hardware_report()
        result = await ai_assistant.analyze_hardware_for_profile(
            hw, req.profile, req.budget, req.session_id
        )
        # Persist session
        session_doc = {
            "id": str(uuid.uuid4()),
            "session_id": result["session_id"],
            "profile": req.profile,
            "budget": req.budget,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "recommendation": result["recommendation"],
        }
        await db.ai_sessions.insert_one(session_doc.copy())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"IA error: {str(e)}")

@api_router.post("/ai/chat")
async def ai_chat(req: AIChatRequest):
    try:
        session_id = req.session_id or str(uuid.uuid4())
        context = hardware.get_full_hardware_report() if req.include_hardware else None
        result = await ai_assistant.chat_with_assistant(req.message, session_id, context)
        await db.ai_chat_messages.insert_one({
            "id": str(uuid.uuid4()),
            "session_id": session_id,
            "user_message": req.message,
            "assistant_response": result["response"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"IA chat error: {str(e)}")

@api_router.get("/ai/sessions")
async def ai_sessions():
    items = await db.ai_sessions.find({}, {"_id": 0}).sort("timestamp", -1).to_list(50)
    return {"sessions": items}

# ---------- Documentation ----------
@api_router.get("/docs/pdf")
async def docs_pdf():
    pdf_bytes = docs.build_documentation_pdf()
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=optidriver_documentacion.pdf"},
    )

# Include router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

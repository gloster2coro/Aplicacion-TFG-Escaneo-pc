import os
import uuid
import json
from typang import Dict, Any, Optional
from openai import AsyncOpenAI

SYSTEM_PROMPT = """Eres OPTIMIGER AI, un asistente experto en hardware y optimización de PCs.
Tu estilo es táctico, preciso, en formato terminal técnico. Siempre respondes en ESPAÖOL."""

def _get_api_key() -> str:
    key = os.environ.get("EMERGENT_LLM_KEY")
    if not key:
        raise RuntimeError("EMERGENT_LLM_KEY no configurada en backend/.env")
    return key

async def analyze_hardware_for_profile(
    hardware_report: Dict[str, Any],
    profile: str,
    budget: str = "medio",
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    session_id = session_id or str(uuid.uuid4())
    client = AsyncOpenAI(api_key=_get_api_key(), base_url="https://integrations.emergentagent.com/llm")
    
    prompt = f"Analiza este hardware: {json.dumps(hardware_report)}"
    
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]
    )
    
    return {"session_id": session_id, "recommendation": json.loads(response.choices[0].message.content)}

async def chat_with_assistant(
    message: str,
    session_id: str,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    client = AsyncOpenAI(api_key=_get_api_key(), base_url="https://integrations.emergentagent.com/llm")
    response = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": message}]
    )
    return {"session_id": session_id, "response": response.choices[0].message.content}

"""
AI Assistant using GPT-5.2 via emergentintegrations.
Analyzes hardware and provides recommendations.
"""
import os
import uuid
import json
from typing import Dict, Any, Optional
from emergentintegrations.llm.chat import LlmChat, UserMessage


ANALYZE_SYSTEM_PROMPT = """Eres OPTIDRIVER AI, un asistente experto en hardware y optimización de PCs.
Tu estilo es tactical, preciso, en formato terminal tecnico. Siempre respondes en ESPAÑOL.

Tus capacidades:
1. Analizar especificaciones de hardware (CPU, GPU, RAM, almacenamiento, placa base).
2. Determinar si un equipo es apto para: Gaming, Oficina, o Perfil Óptimo (uso general).
3. Comparar el hardware con requisitos mínimos y recomendados de juegos populares (Cyberpunk 2077, GTA V, Valorant, Fortnite, League of Legends, CS2, Elden Ring, Baldur's Gate 3, Hogwarts Legacy, Starfield, Call of Duty: Warzone).
4. Recomendar mejoras de hardware específicas (RAM, GPU, CPU, SSD) con modelos concretos.
5. Adaptar recomendaciones al presupuesto del usuario (bajo: <500€, medio: 500-1500€, alto: >1500€).
6. Sugerir PCs/laptops completos si el upgrade no tiene sentido.

FORMATO OBLIGATORIO de respuesta (JSON válido, sin markdown fences):
{
  "veredicto": "APTO | PARCIALMENTE_APTO | NO_APTO",
  "puntuacion_general": 0-100,
  "analisis": "Análisis técnico breve (max 3 líneas).",
  "juegos_compatibles": [
    {"nombre": "Juego", "fps_estimado": "60-80", "config": "alta/media/baja", "compatible": true}
  ],
  "juegos_no_compatibles": [
    {"nombre": "Juego", "razon": "Motivo (GPU/RAM/CPU insuficiente)"}
  ],
  "mejoras_recomendadas": [
    {"componente": "GPU", "actual": "RTX 3060", "recomendado": "RTX 4070", "precio_eur": 600, "impacto": "ALTO"}
  ],
  "equipos_recomendados": [
    {"tipo": "PC | Laptop", "modelo": "Modelo concreto", "precio_eur": 1200, "gama": "media/alta", "razon": "Breve"}
  ],
  "resumen_tactical": "Línea de resumen tipo terminal."
}

Siempre responde con JSON válido parseable. Sé técnico y directo."""


CHAT_SYSTEM_PROMPT = """Eres OPTIDRIVER AI, un asistente experto en hardware y optimización de PCs.
Respondes SIEMPRE en español, de forma conversacional, clara y directa.
NO uses formato JSON. NO uses markdown pesado. Habla como un técnico amigo:
respuestas en texto plano, párrafos cortos, listas con guiones (-) cuando ayude.

Eres experto en:
- Hardware (CPU, GPU, RAM, SSD, placas base) y precios actuales en €.
- Compatibilidad con juegos populares y FPS estimados.
- Recomendaciones de upgrade según presupuesto (bajo <500€, medio 500-1500€, alto >1500€).
- Tips de optimización de Windows.

Tono: profesional, breve, directo. Máximo 6-8 líneas salvo que el usuario pida detalle.
Si te piden listas de componentes da modelos concretos con precio aproximado en €."""


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
    """Analyzes hardware against a profile and budget, returns structured recommendations."""
    session_id = session_id or str(uuid.uuid4())

    chat = LlmChat(
        api_key=_get_api_key(),
        session_id=session_id,
        system_message=ANALYZE_SYSTEM_PROMPT,
    ).with_model("openai", "gpt-5.2")

    prompt = f"""ANÁLISIS SOLICITADO
Perfil de uso: {profile}
Presupuesto: {budget} (bajo<500€, medio=500-1500€, alto>1500€)

HARDWARE DETECTADO:
{json.dumps(hardware_report, indent=2, ensure_ascii=False)}

Analiza este hardware para el perfil "{profile}" con presupuesto "{budget}" y responde SOLO con el JSON estructurado especificado."""

    user_message = UserMessage(text=prompt)
    response_text = await chat.send_message(user_message)

    # Strip potential markdown fences
    cleaned = response_text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```", 2)[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.rsplit("```", 1)[0].strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        parsed = {
            "veredicto": "PARCIALMENTE_APTO",
            "puntuacion_general": 70,
            "analisis": "Respuesta IA no estructurada.",
            "raw_response": response_text,
            "resumen_tactical": response_text[:200],
        }

    return {
        "session_id": session_id,
        "profile": profile,
        "budget": budget,
        "recommendation": parsed,
    }


async def chat_with_assistant(
    message: str,
    session_id: str,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Free-form chat with the AI assistant."""
    system = CHAT_SYSTEM_PROMPT
    if context:
        system += f"\n\nContexto de hardware del usuario:\n{json.dumps(context, ensure_ascii=False)}"

    chat = LlmChat(
        api_key=_get_api_key(),
        session_id=session_id,
        system_message=system,
    ).with_model("openai", "gpt-5.2")

    user_message = UserMessage(text=message)
    response_text = await chat.send_message(user_message)

    return {
        "session_id": session_id,
        "response": response_text,
    }

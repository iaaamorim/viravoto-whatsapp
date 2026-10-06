import os
from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.cognitive_engine import analyze_and_reframe
from app.zapi_client import send_zapi_message
from app.evolution_client import send_whatsapp_message

app = FastAPI(
    title="Viravoto Cognitivo - WhatsApp",
    description="Agente de inteligência artificial para reenquadramento de debates com biconceituais e eleitores indecisos.",
    version="1.1.0"
)

class TestRequest(BaseModel):
    message: str

@app.get("/")
async def health_check():
    return {
        "status": "online",
        "service": "Viravoto Cognitivo",
        "gateway": "Z-API / Evolution API",
        "doc": "Envie mensagens via POST /webhook ou teste via POST /test"
    }

@app.post("/test")
async def test_endpoint(req: TestRequest):
    """
    Endpoint simples para testar o reenquadramento diretamente.
    """
    reply = await analyze_and_reframe(req.message)
    return {"input": req.message, "response": reply}

async def process_and_send_response(sender_phone: str, user_text: str, gateway: str = "zapi"):
    """
    Executa a análise de IA e envia a resposta de volta ao WhatsApp.
    """
    print(f"[PROCESSANDO] Recebido de {sender_phone}: {user_text}")
    reply = await analyze_and_reframe(user_text)
    
    if gateway == "zapi":
        await send_zapi_message(sender_phone, reply)
    else:
        await send_whatsapp_message(sender_phone, reply)

@app.post("/webhook")
async def unified_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Webhook inteligente que detecta se a mensagem veio da Z-API ou da Evolution API.
    """
    try:
        payload = await request.json()
    except Exception:
        return JSONResponse({"status": "invalid_json"}, status_code=400)

    # 1. DETECÇÃO Z-API:
    # A Z-API envia campos como 'phone', 'text', 'fromMe', 'isGroup' diretamente no corpo raiz.
    if "phone" in payload and "text" in payload:
        # Ignora mensagens enviadas pelo próprio robô ou de grupos
        if payload.get("fromMe", False):
            return {"status": "ignored", "reason": "from_me"}
        if payload.get("isGroup", False):
            return {"status": "ignored", "reason": "group_message"}

        sender_phone = payload.get("phone", "")
        text_obj = payload.get("text", {})
        user_text = text_obj.get("message", "") if isinstance(text_obj, dict) else str(text_obj)

        if user_text:
            background_tasks.add_task(process_and_send_response, sender_phone, user_text, "zapi")
            return {"status": "queued", "gateway": "zapi"}

    # 2. DETECÇÃO EVOLUTION API:
    event = payload.get("event")
    if event == "messages.upsert":
        data = payload.get("data", {})
        key = data.get("key", {})
        if key.get("fromMe", False):
            return {"status": "ignored", "reason": "from_me"}
            
        remote_jid = key.get("remoteJid", "")
        message_data = data.get("message", {})
        user_text = (
            message_data.get("conversation") or 
            message_data.get("extendedTextMessage", {}).get("text")
        )
        if user_text:
            background_tasks.add_task(process_and_send_response, remote_jid, user_text, "evolution")
            return {"status": "queued", "gateway": "evolution"}

    return {"status": "ignored", "reason": "unsupported_event_or_media"}

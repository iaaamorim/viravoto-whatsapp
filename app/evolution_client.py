import os
import httpx

EVOLUTION_URL = os.getenv("EVOLUTION_URL", "http://evolution-api:8080")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "viravoto_super_secreta_123")
EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE", "viravoto")

async def send_whatsapp_message(number: str, text: str) -> bool:
    """
    Envia uma mensagem de texto para o número especificado através da Evolution API.
    """
    clean_number = number.replace("@s.whatsapp.net", "").replace("+", "").strip()
    
    headers = {
        "apikey": EVOLUTION_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "number": clean_number,
        "text": text
    }
    
    url = f"{EVOLUTION_URL}/message/sendText/{EVOLUTION_INSTANCE}"
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            return response.status_code in [200, 201]
    except Exception as e:
        print(f"[ERRO Evolution API] Falha ao enviar mensagem para {clean_number}: {e}")
        return False

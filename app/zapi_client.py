import os
import httpx

ZAPI_INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID", "")
ZAPI_INSTANCE_TOKEN = os.getenv("ZAPI_INSTANCE_TOKEN", "")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN", "")

async def send_zapi_message(phone: str, text: str) -> bool:
    """
    Envia uma mensagem de texto usando a API da Z-API.
    """
    if not ZAPI_INSTANCE_ID or not ZAPI_INSTANCE_TOKEN:
        print("[ERRO Z-API] ZAPI_INSTANCE_ID ou ZAPI_INSTANCE_TOKEN não configurados.")
        return False

    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_INSTANCE_TOKEN}/send-text"
    
    headers = {
        "Content-Type": "application/json"
    }
    if ZAPI_CLIENT_TOKEN:
        headers["Client-Token"] = ZAPI_CLIENT_TOKEN

    clean_phone = phone.replace("@s.whatsapp.net", "").replace("+", "").replace("-", "").strip()

    payload = {
        "phone": clean_phone,
        "message": text
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code in [200, 201]:
                print(f"[Z-API] Mensagem enviada com sucesso para {clean_phone}")
                return True
            else:
                print(f"[Z-API ERRO] Status {response.status_code}: {response.text}")
                return False
    except Exception as e:
        print(f"[Z-API EXCEÇÃO] Falha ao enviar para {clean_phone}: {e}")
        return False

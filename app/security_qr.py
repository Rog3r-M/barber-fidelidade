import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional

SECRET_KEY = "sua_chave_secreta_barbearia_super_segura"
ALGORITHM = "HS256"
QR_CODE_EXPIRE_SECONDS = 60

def gerador_token_qrcode(barbearia_id: int, barbeiro_id: int) -> str:
    agora = datetime.now(timezone.utc)
    expiracao = agora + timedelta(seconds=QR_CODE_EXPIRE_SECONDS)
    payload = {
        "barbearia_id": barbearia_id,
        "barbeiro_id": barbeiro_id,
        "iat": agora,
        "exp": expiracao,
        "scope": "qr_carimbo"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def validar_token_qrcode(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("scope") != "qr_carimbo":
            return None
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("QR Code expirado. Peça ao barbeiro para gerar um novo.")
    except jwt.InvalidTokenError:
        raise ValueError("QR Code inválido ou assinado incorretamente.")
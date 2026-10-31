from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import Carimbo, ResgateRecompensa
from app.security_qr import validar_token_qrcode
import uuid

def registrar_novo_carimbo(db: Session, cliente_id: int, token_qr: str) -> dict:
    payload = validar_token_qrcode(token_qr)
    
    novo_carimbo = Carimbo(
        cliente_id=cliente_id,
        barbearia_id=payload["barbearia_id"],
        barbeiro_id=payload["barbeiro_id"],
        token_qr_usado=token_qr
    )
    
    try:
        db.add(novo_carimbo)
        db.commit()
        db.refresh(novo_carimbo)
    except IntegrityError:
        db.rollback()
        raise ValueError("Este QR Code já foi utilizado para registrar um carimbo.")

    total_carimbos = db.query(Carimbo).filter(Carimbo.cliente_id == cliente_id).count()
    resgates_realizados = db.query(ResgateRecompensa).filter(ResgateRecompensa.cliente_id == cliente_id).count()
    
    cortes_ganhos = total_carimbos // 10
    cortes_disponiveis = cortes_ganhos - resgates_realizados
    carimbos_progresso_atual = total_carimbos % 10

    gerou_novo_corte = False
    if total_carimbos > 0 and carimbos_progresso_atual == 0 and cortes_disponiveis > 0:
        gerou_novo_corte = True
        novo_resgate = ResgateRecompensa(
            cliente_id=cliente_id,
            barbearia_id=payload["barbearia_id"],
            codigo_resgate=f"FREE-{uuid.uuid4().hex[:8].upper()}"
        )
        db.add(novo_resgate)
        db.commit()

    return {
        "carimbos_totais": total_carimbos,
        "carimbos_cartela_atual": carimbos_progresso_atual if carimbos_progresso_atual != 0 or cortes_disponiveis == 0 else 10,
        "cortes_disponiveis": cortes_disponiveis,
        "ganhou_corte_nesta_visita": gerou_novo_corte
    }
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import LerQRCodeInput, ValidacaoPontoOutput
from app.services_fidelidade import registrar_novo_carimbo

# É esta variável 'router' que o main.py tenta importar
router = APIRouter(prefix="/fidelidade", tags=["Fidelidade"])


@router.post("/validar-qrcode", response_model=ValidacaoPontoOutput)
def validar_carimbo_cliente(
    dados: LerQRCodeInput,
    cliente_id: int = 1,  # ID padrão para testes
    db: Session = Depends(get_db),
):
    """
    [ENDPOINT DO CLIENTE]
    Valida o token lido via câmera, registra o carimbo na sessão ativa do banco SQL
    e retorna o progresso atualizado da cartela.
    """
    try:
        resultado = registrar_novo_carimbo(
            db=db, cliente_id=cliente_id, token_qr=dados.token_qr
        )

        mensagem_sucesso = (
            "Parabéns! Você completou 10 carimbos e ganhou 1 corte grátis!"
            if resultado["ganhou_corte_nesta_visita"]
            else "Visita validada com sucesso! +1 carimbo adicionado."
        )

        return {
            "sucesso": True,
            "mensagem": mensagem_sucesso,
            "novos_pontos": resultado["carimbos_cartela_atual"],
            "ganhou_corte_gratis": resultado["ganhou_corte_nesta_visita"],
        }

    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err)
        )

from app.security_qr import gerador_token_qrcode

@router.get("/gerar-qrcode-teste")
def gerar_token_teste(barbearia_id: int = 1, barbeiro_id: int = 1):
    """Gera um token JWT temporário válido por 60 segundos."""
    token = gerador_token_qrcode(barbearia_id=barbearia_id, barbeiro_id=barbeiro_id)
    return {"token_qr": token}
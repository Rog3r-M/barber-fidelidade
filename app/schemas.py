from pydantic import BaseModel, Field

class LerQRCodeInput(BaseModel):
    token_qr: str = Field(..., description="Token dinâmico extraído do QR Code da barbearia")

class ValidacaoPontoOutput(BaseModel):
    sucesso: bool
    mensagem: str
    novos_pontos: int
    ganhou_corte_gratis: bool
from fastapi import FastAPI
from app.routers import fidelidade

app = FastAPI(
    title="Barber Loyalty API",
    description="API de Cartão de Fidelidade Digital via QR Code para Barbearias",
    version="1.0.0"
)

# Inclui os endpoints de fidelidade
app.include_router(fidelidade.router)

@app.get("/")
def read_root():
    return {"status": "API de Fidelidade Operacional", "docs": "/docs"}
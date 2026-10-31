# Barber Loyalty API

API RESTful para cartão de fidelidade digital de barbearias via QR Code dinâmico com validação temporal e proteção contra fraudes.

## Tecnologias Utilizadas
- **Python 3.10+**
- **FastAPI** (Framework Web)
- **SQLAlchemy** (ORM / Base de Dados Relacional)
- **SQLite** (Desenvolvimento local)
- **PyJWT** (Geração e validação de tokens temporários com expiração TTL)
- **Pydantic** (Validação de schemas)

## Funcionalidades
- Geração de QR Code temporário assinado criptograficamente (expira em 60s).
- Validação de leitura com bloqueio de reuso de token.
- Acúmulo de carimbos e geração automática de vouchers para cortes gratuitos ao atingir 10 carimbos.

## Como Executar o Projeto

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/Rog3r-M/barber-fidelidade.git](https://github.com/Rog3r-M/barber-fidelidade.git)
   cd barber-fidelidade
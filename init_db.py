from app.database import Base, engine
from app.models import Barbearia, Carimbo, ResgateRecompensa, Usuario

print("Criando tabelas no banco de dados SQLite...")
Base.metadata.create_all(bind=engine)
print("Banco de dados inicializado com sucesso!")
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(20), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    tipo_perfil = Column(String(20), default="cliente")
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    carimbos = relationship("Carimbo", back_populates="cliente", foreign_keys="Carimbo.cliente_id")
    resgates = relationship("ResgateRecompensa", back_populates="cliente")


class Barbearia(Base):
    __tablename__ = "barbearias"

    id = Column(Integer, primary_key=True, index=True)
    nome_fantasia = Column(String(100), nullable=False)
    cnpj = Column(String(18), unique=True, nullable=True)
    criado_em = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    carimbos = relationship("Carimbo", back_populates="barbearia")


class Carimbo(Base):
    __tablename__ = "carimbos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    barbearia_id = Column(Integer, ForeignKey("barbearias.id"), nullable=False)
    barbeiro_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    token_qr_usado = Column(Text, unique=True, nullable=False, index=True)
    data_validacao = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    cliente = relationship("Usuario", foreign_keys=[cliente_id], back_populates="carimbos")
    barbearia = relationship("Barbearia", back_populates="carimbos")


class ResgateRecompensa(Base):
    __tablename__ = "resgates_recompensas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False, index=True)
    barbearia_id = Column(Integer, ForeignKey("barbearias.id"), nullable=False)
    
    codigo_resgate = Column(String(50), unique=True, nullable=False)
    utilizado = Column(Boolean, default=False)
    data_resgate = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    cliente = relationship("Usuario", back_populates="resgates")
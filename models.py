from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class ConcertoDB(Base):
    __tablename__ = "concertos"
    
    id = Column(Integer, primary_key=True, index=True) # ID interno (sessão específica)
    id_site = Column(Integer, index=True, nullable=False) # ID do site da OSESP
    nome = Column(String, index=True, nullable=False)
    data = Column(DateTime, nullable=False)
    local = Column(String, default="Sala São Paulo")

    templates = relationship("TemplateDB", back_populates="concerto")

class TemplateDB(Base):
    __tablename__ = "templates"
    
    id = Column(Integer, primary_key=True, index=True)
    concerto_id = Column(Integer, ForeignKey("concertos.id"))
    tipo = Column(String, nullable=False) # Ex: T-7, T-48, T-4
    conteudo = Column(String, nullable=False)

    concerto = relationship("ConcertoDB", back_populates="templates")
    mensagens = relationship("MensagemDB", back_populates="template")

class UsuarioDB(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    contato = Column(String, unique=True, index=True, nullable=False) # Email ou Telefone
    tipo = Column(String, nullable=False) # Ex: assinante, avulso

    mensagens = relationship("MensagemDB", back_populates="usuario")

class MensagemDB(Base):
    __tablename__ = "mensagens"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    template_id = Column(Integer, ForeignKey("templates.id"))
    data_envio = Column(DateTime, nullable=False)
    provider = Column(String, nullable=False) # Ex: wpp, telegram
    status = Column(String, nullable=False)

    usuario = relationship("UsuarioDB", back_populates="mensagens")
    template = relationship("TemplateDB", back_populates="mensagens")
    respostas = relationship("RespostaDB", back_populates="mensagem")

class RespostaDB(Base):
    __tablename__ = "respostas"
    
    id = Column(Integer, primary_key=True, index=True)
    mensagem_id = Column(Integer, ForeignKey("mensagens.id"))
    resposta = Column(String, nullable=False) # Ex: "Vou comparecer", "Não posso ir"
    timestamp = Column(DateTime, nullable=False)

    mensagem = relationship("MensagemDB", back_populates="respostas")
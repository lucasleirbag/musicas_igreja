from sqlalchemy import Column, Integer, String
from app.database.setup import Base
from pydantic import BaseModel

class Musica(Base):
    __tablename__ = "musicas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    link_spotify = Column(String, index=True)
    link_youtube = Column(String, index=True)
    preferencia_sexta = Column(Integer, default=0)
    preferencia_sabado = Column(Integer, default=0)
    preferencia_domingo = Column(Integer, default=0)

class MusicaBase(BaseModel):
    nome: str
    link_spotify: str
    link_youtube: str
    preferencia_sexta: int
    preferencia_sabado: int
    preferencia_domingo: int

class MusicaCreate(MusicaBase):
    pass

class MusicaResponse(MusicaBase):
    id: int

    class Config:
        orm_mode = True

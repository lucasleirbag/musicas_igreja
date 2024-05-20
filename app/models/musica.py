from sqlalchemy import Column, Integer, String
from app.database.setup import Base
from pydantic import BaseModel

class Musica(Base):
    __tablename__ = "musicas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    link_spotify = Column(String, index=True)
    link_youtube = Column(String, index=True)
    dia_preferencia = Column(String, index=True)

class MusicaBase(BaseModel):
    nome: str
    link_spotify: str
    link_youtube: str
    dia_preferencia: str

class MusicaCreate(MusicaBase):
    pass

class MusicaResponse(MusicaBase):
    id: int

    class Config:
        orm_mode = True

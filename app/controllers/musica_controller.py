from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.setup import SessionLocal
from app.models.musica import Musica, MusicaCreate, MusicaResponse
from app.repositories.musica_repository import MusicaRepository
from app.services.musica_service import MusicaService

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/musicas/", response_model=MusicaResponse)
def criar_musica(musica: MusicaCreate, db: Session = Depends(get_db)):
    musica_repository = MusicaRepository(db)
    musica_service = MusicaService(musica_repository)
    db_musica = Musica(
        nome=musica.nome,
        link_spotify=musica.link_spotify,
        link_youtube=musica.link_youtube,
        dia_preferencia=musica.dia_preferencia
    )
    return musica_service.criar_musica(db_musica)

@router.get("/musicas/{dia}", response_model=list[MusicaResponse])
def obter_musicas(dia: str, db: Session = Depends(get_db)):
    musica_repository = MusicaRepository(db)
    musica_service = MusicaService(musica_repository)
    return musica_service.escolher_musicas(dia, 2 if dia == 'sabado' else 1)

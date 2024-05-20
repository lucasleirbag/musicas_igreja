import random
from sqlalchemy.orm import Session
from app.repositories.musica_repository import MusicaRepository
from app.models.musica import Musica

class MusicaService:
    def __init__(self, musica_repository: MusicaRepository):
        self.musica_repository = musica_repository

    def escolher_musicas(self, dia: str, quantidade: int):
        musicas = self.musica_repository.obter_por_dia(dia)
        return random.sample(musicas, quantidade) if len(musicas) >= quantidade else musicas

    def criar_musica(self, musica: Musica):
        return self.musica_repository.criar(musica)

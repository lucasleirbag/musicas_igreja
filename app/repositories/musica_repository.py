from sqlalchemy.orm import Session
from app.models.musica import Musica

class MusicaRepository:
    def __init__(self, db: Session):
        self.db = db

    def criar(self, musica: Musica):
        self.db.add(musica)
        self.db.commit()
        self.db.refresh(musica)
        return musica

    def obter_todas(self):
        return self.db.query(Musica).all()

    def obter_por_id(self, musica_id: int):
        return self.db.query(Musica).filter(Musica.id == musica_id).first()

    def excluir(self, musica: Musica):
        self.db.delete(musica)
        self.db.commit()

from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.setup import Base

class Sorteio(Base):
    __tablename__ = "sorteios"

    id = Column(Integer, primary_key=True, index=True)
    sorteio_id = Column(Integer, index=True)
    semana = Column(Integer, index=True)
    mes = Column(Integer, index=True)
    ano = Column(Integer, index=True)
    dia = Column(String, index=True)  # Armazena o dia da semana (sexta, domingo)
    musica_id = Column(Integer, ForeignKey('musicas.id'), index=True)
    status = Column(Integer, nullable=True)  # Status 0, 1 ou NULL

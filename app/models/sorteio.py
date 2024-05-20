from sqlalchemy import Column, Integer, String
from app.database.setup import Base

class Sorteio(Base):
    __tablename__ = "sorteios"

    id = Column(Integer, primary_key=True, index=True)
    sorteio_id = Column(Integer, index=True)
    semana = Column(Integer, index=True)
    mes = Column(Integer, index=True)
    ano = Column(Integer, index=True)
    dia = Column(String, index=True)  # Armazena o dia da semana (sexta, hinos_da_ceia, domingo)
    musica_id = Column(Integer, index=True)

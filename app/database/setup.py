from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./musicas.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    from app.models.sorteio import Sorteio  # Importando o modelo Sorteio
    # Drop and create only the sorteios table
    Sorteio.__table__.drop(engine, checkfirst=True)
    Sorteio.__table__.create(engine)

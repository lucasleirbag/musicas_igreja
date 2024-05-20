from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./musicas.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Utilize a nova localização de `declarative_base`
from sqlalchemy.orm import declarative_base
Base = declarative_base()

def init_db():
    import app.models.musica
    Base.metadata.create_all(bind=engine)

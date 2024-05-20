from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.setup import init_db, SessionLocal
from app.models.musica import Musica, MusicaCreate
from app.repositories.musica_repository import MusicaRepository
from app.services.musica_service import MusicaService

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
def startup_event():
    init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, db: Session = Depends(get_db)):
    musica_repository = MusicaRepository(db)
    musicas = musica_repository.obter_todas()
    return templates.TemplateResponse("index.html", {"request": request, "musicas": musicas})

@app.get("/criar_musica", response_class=HTMLResponse)
async def criar_musica_form(request: Request):
    return templates.TemplateResponse("criar_musica.html", {"request": request})

@app.post("/criar_musica", response_class=HTMLResponse)
async def criar_musica(
    request: Request,
    nome: str = Form(...),
    link_spotify: str = Form(...),
    link_youtube: str = Form(...),
    dia_preferencia: str = Form(...),
    db: Session = Depends(get_db)
):
    musica_repository = MusicaRepository(db)
    musica_service = MusicaService(musica_repository)
    db_musica = Musica(
        nome=nome,
        link_spotify=link_spotify,
        link_youtube=link_youtube,
        dia_preferencia=dia_preferencia
    )
    musica_service.criar_musica(db_musica)
    return templates.TemplateResponse("criar_musica.html", {"request": request, "message": "Música criada com sucesso!"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

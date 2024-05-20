from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.setup import init_db, SessionLocal
from app.models.musica import Musica
from app.repositories.musica_repository import MusicaRepository
from app.services.musica_service import MusicaService
from datetime import datetime

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
    preferencia_sexta: int = Form(0),
    preferencia_sabado: int = Form(0),
    preferencia_domingo: int = Form(0),
    db: Session = Depends(get_db)
):
    musica_repository = MusicaRepository(db)
    musica_service = MusicaService(musica_repository)
    db_musica = Musica(
        nome=nome,
        link_spotify=link_spotify,
        link_youtube=link_youtube,
        preferencia_sexta=preferencia_sexta,
        preferencia_sabado=preferencia_sabado,
        preferencia_domingo=preferencia_domingo
    )
    musica_service.criar_musica(db_musica)
    return templates.TemplateResponse("criar_musica.html", {"request": request, "message": "Música criada com sucesso!"})

@app.post("/sortear_musicas_mes", response_class=HTMLResponse)
async def sortear_musicas_mes(request: Request, db: Session = Depends(get_db)):
    musica_repository = MusicaRepository(db)
    musica_service = MusicaService(musica_repository)
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year
    sorteios_do_mes = musica_service.gerar_sorteios_para_o_mes(mes_atual, ano_atual)
    return templates.TemplateResponse("sorteios_mes.html", {
        "request": request,
        "sorteios_do_mes": sorteios_do_mes
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

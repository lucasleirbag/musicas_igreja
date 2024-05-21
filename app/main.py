from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.setup import init_db, get_db
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

@app.get("/editar_musica/{musica_id}", response_class=HTMLResponse)
async def editar_musica_form(request: Request, musica_id: int, db: Session = Depends(get_db)):
    musica_repository = MusicaRepository(db)
    musica = musica_repository.obter_por_id(musica_id)
    if musica is None:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    return templates.TemplateResponse("criar_musica.html", {"request": request, "musica": musica})

@app.post("/editar_musica/{musica_id}", response_class=HTMLResponse)
async def editar_musica(
    request: Request,
    musica_id: int,
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
    db_musica = musica_repository.obter_por_id(musica_id)
    if db_musica is None:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    db_musica.nome = nome
    db_musica.link_spotify = link_spotify
    db_musica.link_youtube = link_youtube
    db_musica.preferencia_sexta = preferencia_sexta
    db_musica.preferencia_sabado = preferencia_sabado
    db_musica.preferencia_domingo = preferencia_domingo
    musica_service.atualizar_musica(db_musica)
    return templates.TemplateResponse("criar_musica.html", {"request": request, "message": "Música atualizada com sucesso!", "musica": db_musica})

@app.post("/excluir_musica/{musica_id}", response_class=HTMLResponse)
async def excluir_musica(request: Request, musica_id: int, db: Session = Depends(get_db)):
    musica_repository = MusicaRepository(db)
    musica_service = MusicaService(musica_repository)
    db_musica = musica_repository.obter_por_id(musica_id)
    if db_musica is None:
        raise HTTPException(status_code=404, detail="Música não encontrada")
    musica_service.excluir_musica(db_musica)
    musicas = musica_repository.obter_todas()
    return templates.TemplateResponse("index.html", {"request": request, "message": "Música excluída com sucesso!", "musicas": musicas})

@app.post("/sortear_musicas_mes", response_class=HTMLResponse)
async def sortear_musicas_mes(request: Request, db: Session = Depends(get_db)):
    musica_repository = MusicaRepository(db)
    musica_service = MusicaService(musica_repository)
    mes_atual = datetime.now().month
    ano_atual = datetime.now().year
    sorteios_do_mes = musica_service.gerar_sorteios_para_o_mes(mes_atual, ano_atual)
    if sorteios_do_mes is None:
        sorteios_do_mes = []
    return templates.TemplateResponse("sorteios_mes.html", {
        "request": request,
        "sorteios_do_mes": sorteios_do_mes
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

import random
from sqlalchemy.orm import Session
from app.repositories.musica_repository import MusicaRepository
from app.models.musica import Musica
from app.models.sorteio import Sorteio

class MusicaService:
    def __init__(self, musica_repository: MusicaRepository):
        self.musica_repository = musica_repository

    def escolher_musicas(self, dia: str, quantidade: int, semana: int, mes: int, ano: int):
        # Obter IDs das músicas sorteadas no mês atual e no mês anterior para o mesmo dia
        musicas_recentemente_sorteadas = self.musica_repository.db.query(Sorteio.musica_id).filter(
            (Sorteio.mes == mes - 1) | (Sorteio.mes == mes),
            (Sorteio.ano == ano),
            (Sorteio.dia == dia)
        ).all()
        musicas_recentemente_sorteadas = [musica[0] for musica in musicas_recentemente_sorteadas]

        # Obter IDs das músicas sorteadas na mesma semana
        musicas_ja_sorteadas_na_semana = self.musica_repository.db.query(Sorteio.musica_id).filter(
            Sorteio.semana == semana,
            Sorteio.mes == mes,
            Sorteio.ano == ano
        ).all()
        musicas_ja_sorteadas_na_semana = [musica[0] for musica in musicas_ja_sorteadas_na_semana]

        # Filtrar músicas de acordo com o dia da preferência e excluir músicas recentemente sorteadas e já sorteadas na semana
        if dia == 'sexta':
            musicas = self.musica_repository.db.query(Musica).filter(
                Musica.preferencia_sexta == 1,
                Musica.id.notin_(musicas_recentemente_sorteadas),
                Musica.id.notin_(musicas_ja_sorteadas_na_semana)
            ).all()
        elif dia == 'hinos_da_ceia':
            musicas = self.musica_repository.db.query(Musica).filter(
                Musica.preferencia_sabado == 1,
                Musica.id.notin_(musicas_recentemente_sorteadas),
                Musica.id.notin_(musicas_ja_sorteadas_na_semana)
            ).all()
        elif dia == 'domingo':
            musicas = self.musica_repository.db.query(Musica).filter(
                Musica.preferencia_domingo == 1,
                Musica.id.notin_(musicas_recentemente_sorteadas),
                Musica.id.notin_(musicas_ja_sorteadas_na_semana)
            ).all()
        else:
            musicas = []

        if len(musicas) < quantidade:
            raise ValueError(f"Não há músicas suficientes para sortear {quantidade} músicas para {dia} sem repetição recente.")

        musicas_sorteadas = random.sample(musicas, quantidade)

        return musicas_sorteadas

    def gerar_sorteios_para_o_mes(self, mes: int, ano: int):
        # Limpar sorteios existentes para o mês
        self.musica_repository.db.query(Sorteio).filter(Sorteio.mes == mes, Sorteio.ano == ano).delete()
        self.musica_repository.db.commit()

        sorteios_do_mes = []

        for semana in range(1, 5):
            for dia in ['sexta', 'hinos_da_ceia', 'domingo']:
                musicas_sorteadas = self.escolher_musicas(dia, 2, semana, mes, ano)
                for musica in musicas_sorteadas:
                    registro = Sorteio(sorteio_id=semana, semana=semana, mes=mes, ano=ano, dia=dia, musica_id=musica.id)
                    self.musica_repository.db.add(registro)
                    sorteios_do_mes.append((semana, dia, musica.nome))

        self.musica_repository.db.commit()
        return sorteios_do_mes

    def criar_musica(self, musica: Musica):
        return self.musica_repository.criar(musica)

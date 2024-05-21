import random
from sqlalchemy.orm import Session
from app.repositories.musica_repository import MusicaRepository
from app.models.musica import Musica
from app.models.sorteio import Sorteio

class MusicaService:
    def __init__(self, musica_repository: MusicaRepository):
        self.musica_repository = musica_repository

    def escolher_musicas(self, dia: str, quantidade: int, semana: int, mes: int, ano: int, excluidos: list):
        # Obter IDs das músicas disponíveis para sorteio (status diferente de 0 ou 1)
        musicas_disponiveis = self.musica_repository.db.query(Musica).filter(
            Musica.id.notin_(
                self.musica_repository.db.query(Sorteio.musica_id).filter(Sorteio.status.in_([0, 1]))
            ),
            Musica.id.notin_(excluidos)
        ).all()

        if len(musicas_disponiveis) < quantidade:
            raise ValueError(f"Não há músicas suficientes para sortear {quantidade} músicas para {dia} sem repetição recente.")

        musicas_sorteadas = random.sample(musicas_disponiveis, quantidade)

        for musica in musicas_sorteadas:
            # Adicionar o sorteio com status 0
            sorteio = Sorteio(
                sorteio_id=semana,
                semana=semana,
                mes=mes,
                ano=ano,
                dia=dia,
                musica_id=musica.id,
                status=0
            )
            self.musica_repository.db.add(sorteio)

        self.musica_repository.db.commit()

        return [(musica.id, musica.nome, musica.link_spotify, musica.link_youtube) for musica in musicas_sorteadas]

    def gerar_sorteios_para_o_mes(self, mes: int, ano: int):
        sorteios_do_mes = []

        for semana in range(1, 5):
            excluidos = []
            for dia in ['sexta', 'domingo']:
                musicas_sorteadas = self.escolher_musicas(dia, 2, semana, mes, ano, excluidos)
                excluidos.extend([musica[0] for musica in musicas_sorteadas])
                sorteios_do_mes.append((semana, dia, musicas_sorteadas))
            
            # Atualizar status das músicas sorteadas na semana atual
            self.musica_repository.db.query(Sorteio).filter(
                Sorteio.semana == semana,
                Sorteio.mes == mes,
                Sorteio.ano == ano,
                Sorteio.status == 0
            ).update({"status": 1}, synchronize_session=False)
            
            self.musica_repository.db.commit()

            # Resetar status das músicas sorteadas na semana anterior
            semana_anterior = semana - 1 if semana > 1 else 4
            self.musica_repository.db.query(Sorteio).filter(
                Sorteio.semana == semana_anterior,
                Sorteio.mes == mes,
                Sorteio.ano == ano,
                Sorteio.status == 1
            ).update({"status": None}, synchronize_session=False)
            
            self.musica_repository.db.commit()

        # Sortear hinos para um sábado específico (ceia do Senhor)
        hinos_sabado = self.escolher_musicas('hinos_da_ceia', 2, 5, mes, ano, [])
        sorteios_do_mes.append((5, 'hinos_da_ceia', hinos_sabado))

        return sorteios_do_mes

    def criar_musica(self, musica: Musica):
        return self.musica_repository.criar(musica)

    def atualizar_musica(self, musica: Musica):
        self.musica_repository.db.commit()

    def excluir_musica(self, musica: Musica):
        self.musica_repository.db.delete(musica)
        self.musica_repository.db.commit()

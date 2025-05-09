from typing import List, Dict
from models.semente import Semente

class Casa:
    """Representa um buraco do tabuleiro que contém sementes."""
    def __init__(self):
        self.sementes: List[Semente] = []

    def adicionar_semente(self, tipo_semente: int, quantidade: int = 1) -> None:
        """Adiciona sementes do tipo especificado na quantidade indicada"""
        for _ in range(quantidade):
            self.sementes.append(Semente(tipo_semente))

    def retirar_todas(self) -> Dict[int, int]:
        """Retorna um dicionário com contagem de sementes por tipo e esvazia a casa"""
        sementes_por_tipo = {}
        for semente in self.sementes:
            tipo = semente.tipo
            if tipo in sementes_por_tipo:
                sementes_por_tipo[tipo] += 1
            else:
                sementes_por_tipo[tipo] = 1
        self.sementes = []
        return sementes_por_tipo

    def contar(self) -> int:
        return len(self.sementes)

    def esta_vazia(self) -> bool:
        return len(self.sementes) == 0
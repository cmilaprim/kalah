from typing import List
from models.semente import Semente

class Casa:
    """Representa um buraco do tabuleiro que contém sementes."""
    def __init__(self):
        self.sementes: List[Semente] = []

    def adicionar_semente(self, quantidade: int = 1) -> None:
        """Adiciona sementes na quantidade indicada"""
        for _ in range(quantidade):
            self.sementes.append(Semente())

    def retirar_todas(self) -> List[Semente]:
        """Retorna a lista de sementes e esvazia a casa"""
        sementes = self.sementes.copy()
        self.sementes = []
        return sementes

    def contar(self) -> int:
        return len(self.sementes)

    def esta_vazia(self) -> bool:
        return len(self.sementes) == 0
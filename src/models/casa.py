from models.semente import Semente
from typing import List

class Casa:
    """Representa um buraco do tabuleiro que contém sementes."""
    def __init__(self):
        self.sementes: List[Semente] = []

    def adicionar_semente(self, s: Semente) -> None:
        self.sementes.append(s)

    def retirar_todas(self) -> List[Semente]:
        todas = self.sementes
        self.sementes = []
        return todas

    def contar(self) -> int:
        return len(self.sementes)

    def esta_vazia(self) -> bool:
        return len(self.sementes) == 0
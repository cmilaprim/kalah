from models.semente import Semente
from typing import List


class Armazem:
    """Representa o armazém que acumula sementes capturadas."""
    def __init__(self):
        self.sementes: List[Semente] = []

    def adicionar_semente(self, sementes: List[Semente]) -> None:
        self.sementes.extend(sementes)

    def contar(self) -> int:
        return len(self.sementes)
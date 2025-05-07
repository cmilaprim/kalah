from typing import Dict

from typing import Dict
from models.semente import Semente

class Casa:
    """Representa um buraco do tabuleiro que contém sementes."""
    def __init__(self):
        # Armazena a quantidade de cada tipo de semente
        self.sementes_por_tipo: Dict[int, int] = {1: 0, 2: 0}

    def adicionar_semente(self, tipo: int, quantidade: int = 1) -> None:
        self.sementes_por_tipo[tipo] += quantidade

    def retirar_todas(self) -> Dict[int, int]:
        # Retorna um dicionário com as quantidades retiradas
        retiradas = self.sementes_por_tipo.copy()
        self.sementes_por_tipo = {1: 0, 2: 0}
        return retiradas

    def contar(self) -> int:
        return sum(self.sementes_por_tipo.values())

    def esta_vazia(self) -> bool:
        return self.contar() == 0
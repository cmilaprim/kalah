from typing import Dict
from models.semente import Semente

class Armazem:
    """Representa o armazém que acumula sementes capturadas."""
    def __init__(self):
        # Armazena a quantidade de cada tipo de semente
        self.sementes_por_tipo: Dict[int, int] = {1: 0, 2: 0}

    def adicionar_semente(self, tipo: int, quantidade: int = 1) -> None:
        self.sementes_por_tipo[tipo] += quantidade

    def contar(self) -> int:
        return sum(self.sementes_por_tipo.values())
        
    def contar_por_tipo(self, tipo: int) -> int:
        return self.sementes_por_tipo[tipo]
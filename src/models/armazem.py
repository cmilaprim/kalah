from typing import List
from models.semente import Semente

class Armazem:
    """Representa o armazém que acumula sementes capturadas."""
    def __init__(self):
        self.sementes: List[Semente] = []

    def adicionar_semente(self, tipo_semente: int, quantidade: int = 1) -> None:
        """Adiciona sementes do tipo especificado na quantidade indicada"""
        for _ in range(quantidade):
            self.sementes.append(Semente(tipo_semente))
        
    def contar(self) -> int:
        return len(self.sementes)
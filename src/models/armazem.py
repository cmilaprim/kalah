from typing import List
from models.semente import Semente

class Armazem:
    """Representa o armazém que acumula sementes capturadas."""
    def __init__(self):
        self.sementes: List[Semente] = []

    def adicionar_semente(self, quantidade: int = 1) -> None:
        """Adiciona sementes na quantidade indicada"""
        for _ in range(quantidade):
            self.sementes.append(Semente())
    
    def adicionar_sementes_lista(self, sementes: List[Semente]) -> None:
        """Adiciona uma lista de sementes ao armazém"""
        self.sementes.extend(sementes)
        
    def contar(self) -> int:
        return len(self.sementes)
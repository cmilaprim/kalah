from typing import List
from models.armazem import Armazem
from models.casa import Casa


class Jogador:
    """Um jogador tem 6 casas e 1 armazém."""
    def __init__(self, numero: int):
        self.numero = numero
        self.casas: List[Casa] = [Casa() for _ in range(6)]
        self.armazem: Armazem = Armazem()
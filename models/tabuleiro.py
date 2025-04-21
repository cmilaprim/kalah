# model/tabuleiro.py
from typing import List, Optional
from models.semente import Semente

class Tabuleiro:
    def __init__(self):
        #cada lado é uma lista de 6 casas e cada casa é uma lista de 4 sementes do respectivo jogador:
        lado1 = [[Semente(1) for _ in range(4)] for _ in range(6)]
        lado2 = [[Semente(2) for _ in range(4)] for _ in range(6)]
        #agora self.casas é uma lista mutável de dois elementos:
        self.casas: List[List[List[Semente]]] = [lado1, lado2]

        #armazéns começam vazios — lista mutável de duas listas:
        self.armazens: List[List[Semente]] = [[], []]

        #jogador_atual = 1 ou 2
        self.jogador_atual: int = 1

    def estado_em_lista(self) -> List[List[int]]:
        # retorna 12 listas, cada lista = [1,2,1,1,…] indicando o dono de cada semente
        return [
            [s.jogador for s in casa]
            for lado in self.casas
            for casa in lado
        ]

    def armazens_em_lista(self) -> List[List[int]]:
        # retorna dois arrays de donos para cada armazém
        return [
            [s.jogador for s in self.armazens[0]],
            [s.jogador for s in self.armazens[1]]
        ]

    def jogada_valida(self, casa_index: int) -> bool:
        lado = 0 if self.jogador_atual == 1 else 1
        idx  = casa_index if lado == 0 else casa_index - 6
        return 0 <= idx < 6 and len(self.casas[lado][idx]) > 0

    def semear(self, casa_index: int) -> bool:
        #define o lado (0 = Jogador1, 1 = Jogador2) e índice local (0..5)
        lado      = 0 if self.jogador_atual == 1 else 1
        idx_local = casa_index if lado == 0 else casa_index - 6

        #colhe todas as sementes da casa escolhida
        sementes_na_mao = self.casas[lado][idx_local]
        self.casas[lado][idx_local] = []

        #monta o caminho de semeadura (path) SEMPRE em direção ao próprio armazém:
        path: List[tuple] = []
        if lado == 0:
            # --- jogador 1 (topo) semeia ANTI‑HORÁRIO ---
            # a) casas à ESQUERDA na linha de cima
            for j in range(idx_local - 1, -1, -1):
                path.append(("pit", 0, j))
            # b) próprio armazém
            path.append(("store", 0, None))
            # c) todas as casas do adversário, da esquerda para a direita
            for j in range(6):
                path.append(("pit", 1, j))
            # d) completa o ciclo: casas à DIREITA na linha de cima
            for j in range(5, idx_local, -1):
                path.append(("pit", 0, j))

        else:
            # --- Jogador 2 (baixo) semeia HORÁRIO ---
            # a) casas à DIREITA na linha de baixo
            for j in range(idx_local + 1, 6):
                path.append(("pit", 1, j))
            # b) próprio armazém
            path.append(("store", 1, None))
            # c) todas as casas do adversário, da direita para a esquerda
            for j in range(5, -1, -1):
                path.append(("pit", 0, j))
            # d) completa o ciclo: casas à ESQUERDA na linha de baixo
            for j in range(0, idx_local):
                path.append(("pit", 1, j))

        #distribui as sementes seguindo o path em looping
        última_pos = None
        k = 0
        while sementes_na_mao:
            tipo, s, j = path[k % len(path)]
            if tipo == "pit":
                self.casas[s][j].append(sementes_na_mao.pop(0))
            else:  # store
                self.armazens[s].append(sementes_na_mao.pop(0))
            última_pos = (tipo, s, j)
            k += 1

        #captura: se a última caiu em um buraco vazio do próprio lado
        if última_pos[0] == "pit" and última_pos[1] == lado:
            _, _, j = última_pos
            if len(self.casas[lado][j]) == 1:
                opp_j = 5 - j
                if self.casas[1 - lado][opp_j]:
                    # move tudo para o armazém
                    self.armazens[lado].extend(
                        self.casas[1 - lado][opp_j] + self.casas[lado][j]
                    )
                    self.casas[1 - lado][opp_j] = []
                    self.casas[lado][j] = []

        #fim de jogo: um dos lados ficou sem sementes nas casas
        if all(len(c) == 0 for c in self.casas[0]) or all(len(c) == 0 for c in self.casas[1]):
            # recolhe o resto
            for j in range(6):
                self.armazens[0].extend(self.casas[0][j])
                self.casas[0][j] = []
                self.armazens[1].extend(self.casas[1][j])
                self.casas[1][j] = []
            return False  # não há turno extra

        #turno extra?
        return (última_pos[0] == "store" and última_pos[1] == lado)

    def _sync_from_poços(self, poços: List[List[Semente]]):
        #redistribui poços de volta em self.casas e self.armazens
        self.casas[0] = poços[0:6]
        self.armazens[0] = poços[6]
        self.casas[1] = poços[7:13]
        self.armazens[1] = poços[13]

    def jogo_terminou(self) -> bool:
        return all(len(c) == 0 for c in self.casas[0]) or all(len(c) == 0 for c in self.casas[1])

    def obter_vencedor(self) -> Optional[int]:
        a, b = len(self.armazens[0]), len(self.armazens[1])
        if a > b: return 1
        if b > a: return 2
        return None

    def alternar_turno(self, extra: bool):
        if not extra:
            self.jogador_atual = 2 if self.jogador_atual == 1 else 1
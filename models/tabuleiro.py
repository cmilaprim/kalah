# model/tabuleiro.py
from typing import List, Optional
from models.semente import Semente

class Tabuleiro:
    def __init__(self):
        # 1) Cada lado é uma LISTA (não tupla!) de 6 casas,
        #    e cada casa é uma lista de 4 sementes do respectivo jogador:
        lado1 = [[Semente(1) for _ in range(4)] for _ in range(6)]
        lado2 = [[Semente(2) for _ in range(4)] for _ in range(6)]
        # Agora self.casas é uma lista mutável de dois elementos:
        self.casas: List[List[List[Semente]]] = [lado1, lado2]

        # 2) Armazéns começam vazios — lista mutável de duas listas:
        self.armazens: List[List[Semente]] = [[], []]

        # jogador_atual = 1 ou 2
        self.jogador_atual: int = 0

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
        # retira sementes da casa escolhida
        lado = 0 if self.jogador_atual == 1 else 1
        idx  = casa_index if lado == 0 else casa_index - 6
        sementes_na_mao = self.casas[lado][idx]
        self.casas[lado][idx] = []

        # cria lista linear de “poços” (6 casas P1, armazém P1, 6 casas P2, armazém P2)
        poços: List[List[Semente]] = (
            [self.casas[0][i] for i in range(6)] +
            [self.armazens[0]] +
            [self.casas[1][i] for i in range(6)] +
            [self.armazens[1]]
        )

        # mapa de casa_index → índice em poços
        flat_idx = idx if lado == 0 else idx + 7  # +7 pula armazém P1
        own_store = 6 if lado == 0 else 13
        opp_store = 13 if lado == 0 else 6

        # semeia pulando armazém adversário
        while sementes_na_mao:
            flat_idx = (flat_idx + 1) % 14
            if flat_idx == opp_store:
                continue
            poços[flat_idx].append(sementes_na_mao.pop(0))

        last = flat_idx

        # captura
        if last != own_store:
            # caiu num buraco do lado do jogador atual?
            if (lado == 0 and 0 <= last < 6 or
                lado == 1 and 7 <= last < 13) and len(poços[last]) == 1:
                opp = 12 - last
                if poços[opp]:
                    # move todas as sementes (incluindo a que acabou de cair)
                    self.armazens[lado].extend(poços[opp] + poços[last])
                    poços[opp].clear()
                    poços[last].clear()

        # fim de jogo?
        if all(len(poços[i]) == 0 for i in range(6)) or all(len(poços[i]) == 0 for i in range(7,13)):
            # recolhe o resto
            self.armazens[0].extend(poços[i] for i in range(6))
            self.armazens[1].extend(poços[i] for i in range(7,13))
            for i in list(range(6)) + list(range(7,13)):
                poços[i].clear()
            # atualiza casas
            self._sync_from_poços(poços)
            return False

        # atualiza casas e armazéns a partir de poços
        self._sync_from_poços(poços)

        # turno extra?
        return last == own_store

    def _sync_from_poços(self, poços: List[List[Semente]]):
        # re-distribui poços de volta em self.casas e self.armazens
        self.casas[0] = poços[0:6]
        self.armazens[0] = poços[6]
        self.casas[1] = poços[7:13]
        self.armazens[1] = poços[13]

    def jogo_terminou(self) -> bool:
        return all(len(c) == 0 for c in self.casas[0]) or \
               all(len(c) == 0 for c in self.casas[1])

    def obter_vencedor(self) -> Optional[int]:
        a, b = len(self.armazens[0]), len(self.armazens[1])
        if a > b: return 1
        if b > a: return 2
        return None

    def alternar_turno(self, extra: bool):
        if not extra:
            self.jogador_atual = 2 if self.jogador_atual == 1 else 1
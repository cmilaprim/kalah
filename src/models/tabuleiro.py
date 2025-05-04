from typing import List, Optional, Tuple
from models.semente import Semente
from models.casa import Casa
from models.armazem import Armazem
from models.jogador import Jogador

class Tabuleiro:
    def __init__(self):
        self.jogadores: List[Jogador] = [Jogador(1),Jogador(2)]
        self._inicializar_casas()
        self.jogador_atual: int = 1

    def _inicializar_casas(self) -> None:
        for jogador in self.jogadores:
            for casa in jogador.casas:
                for _ in range(4):
                    casa.adicionar_semente(Semente(jogador.numero))

    def estado_em_lista(self) -> List[List[int]]:
        resultado = []
        for jogador in self.jogadores:
            for casa in jogador.casas:
                resultado.append([s.jogador for s in casa.sementes])
        return resultado

    def armazens_em_lista(self) -> List[List[int]]:
        return [
            [s.jogador for s in self.jogadores[0].armazem.sementes],
            [s.jogador for s in self.jogadores[1].armazem.sementes]
        ]

    def jogada_valida(self, casa_index: int) -> bool:
        idx_jogador = 0 if self.jogador_atual == 1 else 1
        idx_casa = casa_index if idx_jogador == 0 else casa_index - 6
        return 0 <= idx_casa < 6 and not self.jogadores[idx_jogador].casas[idx_casa].esta_vazia()

    def semear(self, casa_index: int) -> bool:
        idx_jogador = 0 if self.jogador_atual == 1 else 1
        idx_casa = casa_index if idx_jogador == 0 else casa_index - 6

        # Pegar todas as sementes da casa selecionada
        sementes_na_mao = self.jogadores[idx_jogador].casas[idx_casa].retirar_todas()

        # Construir o caminho de distribuição
        path: List[Tuple[str, int, int]] = []
        if idx_jogador == 0:
            for j in range(idx_casa - 1, -1, -1):
                path.append(("pit", 0, j))
            path.append(("store", 0, None))
            for j in range(6):
                path.append(("pit", 1, j))
            for j in range(5, idx_casa, -1):
                path.append(("pit", 0, j))
        else:
            for j in range(idx_casa + 1, 6):
                path.append(("pit", 1, j))
            path.append(("store", 1, None))
            for j in range(5, -1, -1):
                path.append(("pit", 0, j))
            for j in range(0, idx_casa):
                path.append(("pit", 1, j))

        path = [
                (tipo, idx_jog, j)
                for (tipo, idx_jog, j) in path
                if not (tipo == "store" and idx_jog != idx_jogador)
            ]

        # Distribuir as sementes
        última_pos = None
        k = 0
        while sementes_na_mao:
            tipo, idx_jog, j = path[k % len(path)]
            semente = sementes_na_mao.pop(0)
            
            if tipo == "pit":
                self.jogadores[idx_jog].casas[j].adicionar_semente(semente)
            else:
                self.jogadores[idx_jog].armazem.adicionar_semente([semente])
                
            última_pos = (tipo, idx_jog, j)
            k += 1

        # Captura
        tipo, idx_jog, j = última_pos
        if tipo == "pit" and idx_jog == idx_jogador and self.jogadores[idx_jog].casas[j].contar() == 1:
            opp_jog = 1 - idx_jog
            opp_j = j
            if not self.jogadores[opp_jog].casas[opp_j].esta_vazia():
                # Capturar sementes opostas
                sementes_oponente = self.jogadores[opp_jog].casas[opp_j].retirar_todas()
                self.jogadores[idx_jog].armazem.adicionar_semente(sementes_oponente)

        # Verificar fim de jogo
        # if self.jogo_terminou():
        #     for idx_jog in range(2):
        #         for j in range(6):
        #             sementes = self.jogadores[idx_jog].casas[j].retirar_todas()
        #             self.jogadores[idx_jog].armazem.adicionar_semente(sementes)
        #     return False

        return (última_pos[0] == "store" and última_pos[1] == idx_jogador)
    
    def finalizar_jogo(self) -> Optional[int]:
        """
        Coleta todas as sementes que ainda estão nas casas e
        devolve o vencedor com base no total de sementes nos armazéns.
        """
        # (1) mover todas as sementes das 6 casas de cada jogador para seu armazém
        for jogador in self.jogadores:
            for casa in jogador.casas:
                sementes = casa.retirar_todas()
                jogador.armazem.adicionar_semente(sementes)
        # (2) retorna quem tem mais sementes
        return self.obter_vencedor()

    def jogo_terminou(self) -> bool:
        return (all(casa.esta_vazia() for casa in self.jogadores[0].casas) or 
                all(casa.esta_vazia() for casa in self.jogadores[1].casas))

    def obter_vencedor(self) -> Optional[int]:
        a = self.jogadores[0].armazem.contar()
        b = self.jogadores[1].armazem.contar()
        if a > b: return 1
        if b > a: return 2
        return None

    def alternar_turno(self, extra: bool):
        if not extra:
            self.jogador_atual = 2 if self.jogador_atual == 1 else 1
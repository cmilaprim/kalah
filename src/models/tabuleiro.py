from typing import List, Optional, Tuple
from models.jogador import Jogador
from models.semente import Semente   
from models.estado_partida import EstadoPartida
class Tabuleiro:
    def __init__(self):
        self.jogadores: List[Jogador] = [Jogador(1),Jogador(2)]
        self.partida_inciada = True
        self.inicializar_casas()
        self.jogador_atual: int = 1

    def inicializar_casas(self) -> None:
        for jogador in self.jogadores:
            for casa in jogador.casas:
                casa.adicionar_semente(4)
    
    def obter_estado_partida(self) -> EstadoPartida:
        if self.jogo_terminou():
            return EstadoPartida.ENCERRADA
        return EstadoPartida.EM_PROGRESSO

    def estado_em_lista(self) -> List[List[int]]:
        resultado = []
        for jogador in self.jogadores:
            for casa in jogador.casas:
                resultado.append([casa.contar()]) 
        return resultado

    def armazens_em_lista(self) -> List[List[int]]:
        return [
            [self.jogadores[0].armazem.contar()],  
            [self.jogadores[1].armazem.contar()]  
        ]

    def jogada_valida(self, casa_index: int) -> bool:
        if self.jogador_atual == 1:
            # Jogador 1 só pode jogar em casas 0-5
            if not (0 <= casa_index <= 5):
                return False
            return not self.jogadores[0].casas[casa_index].esta_vazia()
        
        else:  # jogador_atual == 2
            # Jogador 2 só pode jogar em casas 6-11
            if not (6 <= casa_index <= 11):
                return False
            idx_casa = casa_index - 6  # Converte para índice 0-5
            return not self.jogadores[1].casas[idx_casa].esta_vazia()
    
    def semear(self, casa_index: int) -> bool:
        idx_jog, idx_casa = self.ajustar_indices(casa_index)
        sementes_na_mao = self.jogadores[idx_jog].casas[idx_casa].retirar_todas()
        self.ultimo_caminho = self.construir_caminho(idx_jog, idx_casa)
        ultima_pos = self.distribuir_sementes(self.ultimo_caminho, sementes_na_mao)
        self.verificar_captura(ultima_pos)
        return ultima_pos[0] == "armazem" and ultima_pos[1] == idx_jog
        
    def ajustar_indices(self, casa_index: int) -> tuple[int, int]:
        idx_jog = 0 if self.jogador_atual == 1 else 1
        idx_casa = casa_index if idx_jog == 0 else casa_index - 6
        return idx_jog, idx_casa
    
    def construir_caminho(self, idx_jog: int, idx_casa: int) -> list[tuple[str,int,int]]:
        path: list[tuple[str,int,int]] = []
        if idx_jog == 0:
            # semear no sentido anti-horário a partir de idx_casa
            for j in range(idx_casa-1, -1, -1):
                path.append(("casa", 0, j))
            path.append(("armazem", 0, None))
            for j in range(6):
                path.append(("casa", 1, j))
            for j in range(5, idx_casa, -1):
                path.append(("casa", 0, j))
        else:
            # análogo para o segundo jogador
            for j in range(idx_casa+1, 6):
                path.append(("casa", 1, j))
            path.append(("armazem", 1, None))
            for j in range(5, -1, -1):
                path.append(("casa", 0, j))
            for j in range(0, idx_casa):
                path.append(("casa", 1, j))

        # remove o armazém adversário do caminho
        return [
            (t, ij, j) for (t, ij, j) in path
            if not (t == "armazem" and ij != idx_jog)
        ]
    
    def distribuir_sementes(self, path, sementes_lista: List[Semente]) -> tuple[str,int,int]:
        última_pos = None
        k = 0
        
        for semente in sementes_lista:
            tipo_lugar, idx_jog, j = path[k % len(path)]
            
            if tipo_lugar == "casa":
                self.jogadores[idx_jog].casas[j].adicionar_semente(1)
            else:  
                self.jogadores[idx_jog].armazem.adicionar_semente(1)
                
            última_pos = (tipo_lugar, idx_jog, j)
            k += 1
            
        return última_pos
    
    def verificar_captura(self, última_pos: tuple[str,int,int]) -> None:
        tipo, idx_jog, j = última_pos
        
        if (tipo == "casa" and 
            idx_jog == (0 if self.jogador_atual == 1 else 1) and 
            self.jogadores[idx_jog].casas[j].contar() == 1):
            
            opp_idx = 1 - idx_jog
            casa_oposta = self.jogadores[opp_idx].casas[j]
            
            if not casa_oposta.esta_vazia():
                sementes_oponente = casa_oposta.retirar_todas()
                semente_propria = self.jogadores[idx_jog].casas[j].retirar_todas()
                
                self.jogadores[idx_jog].armazem.adicionar_sementes_lista(sementes_oponente)
                self.jogadores[idx_jog].armazem.adicionar_sementes_lista(semente_propria)


    def finalizar_jogo(self) -> Optional[int]:
        """
        Coleta todas as sementes que ainda estão nas casas e
        devolve o vencedor com base no total de sementes nos armazéns.
        """        
        # Coleta sementes restantes nas casas
        for idx, jogador in enumerate(self.jogadores):
            sementes_coletadas = 0
            for casa_idx, casa in enumerate(jogador.casas):
                if not casa.esta_vazia():
                    sementes = casa.retirar_todas()
                    jogador.armazem.adicionar_sementes_lista(sementes)
                    sementes_coletadas += len(sementes)
                
        return self.obter_vencedor()

    def jogo_terminou(self) -> bool:
        return (all(casa.esta_vazia() for casa in self.jogadores[0].casas) or all(casa.esta_vazia() for casa in self.jogadores[1].casas))

    def obter_vencedor(self) -> Optional[int]:
        a = self.jogadores[0].armazem.contar()
        b = self.jogadores[1].armazem.contar()
        if a > b: return 1
        if b > a: return 2
        return None

    def alternar_turno(self, extra: bool):
        if not extra:
            self.jogador_atual = 2 if self.jogador_atual == 1 else 1
    
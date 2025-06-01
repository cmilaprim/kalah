from typing import List, Optional, Tuple
from models.jogador import Jogador
from models.semente import Semente   
from models.status_jogo import EstadoPartida
class Tabuleiro:
    def __init__(self):
        self.jogadores: List[Jogador] = [
            Jogador(1),
            Jogador(2)
        ]
        self.partida_inciada = True
        self.inicializar_casas()
        self.jogador_atual: int = 1

    def inicializar_casas(self) -> None:
        for jogador in self.jogadores:
            for casa in jogador.casas:
                # Adiciona 2 sementes de cada tipo
                casa.adicionar_semente(1, 2)
                casa.adicionar_semente(2, 2)
    
    def obter_estado_partida(self) -> EstadoPartida:
        pass

    def jogada_valida(self, casa_index: int) -> bool:
        pass

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
        idx_jogador = 0 if self.jogador_atual == 1 else 1
        idx_casa = casa_index if idx_jogador == 0 else casa_index - 6
        return 0 <= idx_casa < 6 and not self.jogadores[idx_jogador].casas[idx_casa].esta_vazia()
    
    def semear(self, casa_index: int) -> bool:
        idx_jog, idx_casa = self.ajustar_indices(casa_index)
        sementes_na_mao = self.jogadores[idx_jog].casas[idx_casa].retirar_todas()
        self.ultimo_caminho = self.construir_caminho(idx_jog, idx_casa)
        ultima_pos = self.distribuir_sementes(self.ultimo_caminho, sementes_na_mao)
        self.verificar_captura(ultima_pos)
        return ultima_pos[0] == "store" and ultima_pos[1] == idx_jog
        
    def ajustar_indices(self, casa_index: int) -> tuple[int, int]:
        idx_jog = 0 if self.jogador_atual == 1 else 1
        idx_casa = casa_index if idx_jog == 0 else casa_index - 6
        return idx_jog, idx_casa
    
    def construir_caminho(self, idx_jog: int, idx_casa: int) -> list[tuple[str,int,int]]:
        path: list[tuple[str,int,int]] = []
        if idx_jog == 0:
            # semear no sentido anti-horário a partir de idx_casa
            for j in range(idx_casa-1, -1, -1):
                path.append(("pit", 0, j))
            path.append(("store", 0, None))
            for j in range(6):
                path.append(("pit", 1, j))
            for j in range(5, idx_casa, -1):
                path.append(("pit", 0, j))
        else:
            # análogo para o segundo jogador
            for j in range(idx_casa+1, 6):
                path.append(("pit", 1, j))
            path.append(("store", 1, None))
            for j in range(5, -1, -1):
                path.append(("pit", 0, j))
            for j in range(0, idx_casa):
                path.append(("pit", 1, j))

        # remove o armazém adversário do caminho
        return [
            (t, ij, j) for (t, ij, j) in path
            if not (t == "store" and ij != idx_jog)
        ]
    
    def get_caminho_semeadura(self) -> list[int]:
        return [
            ij * 6 + j
            for (t, ij, j) in self.ultimo_caminho
            if t == "pit"
        ]
    
    def distribuir_sementes(self, path, sementes_dict) -> tuple[str,int,int]:
        última_pos = None
        k = 0
        
        # Converter o dicionário em uma lista de sementes
        sementes = []
        for tipo, quantidade in sementes_dict.items():
            for _ in range(quantidade):
                sementes.append(Semente(tipo))
        
        # Total de sementes
        total_sementes = len(sementes)
        
        while total_sementes > 0:
            tipo_lugar, idx_jog, j = path[k % len(path)]
            
            # Pega a próxima semente da lista
            semente = sementes.pop(0)
            
            if tipo_lugar == "pit":
                self.jogadores[idx_jog].casas[j].adicionar_semente(semente.tipo, 1)
            else:  # store
                self.jogadores[idx_jog].armazem.adicionar_semente(semente.tipo, 1)
                
            total_sementes -= 1
            última_pos = (tipo_lugar, idx_jog, j)
            k += 1
            
        return última_pos
    
    def verificar_captura(self, última_pos: tuple[str,int,int]) -> None:
        tipo, idx_jog, j = última_pos
        
        if (tipo == "pit" and 
            idx_jog == (0 if self.jogador_atual == 1 else 1) and 
            self.jogadores[idx_jog].casas[j].contar() == 1):
            
            opp_idx = 1 - idx_jog
            sementes_oponente = self.jogadores[opp_idx].casas[j].retirar_todas()
            # Adiciona as sementes capturadas ao armazém
            for tipo_semente, quantidade in sementes_oponente.items():
                if quantidade > 0:
                    self.jogadores[idx_jog].armazem.adicionar_semente(tipo_semente, quantidade)
            
    
    def finalizar_jogo(self) -> Optional[int]:
        """
        Coleta todas as sementes que ainda estão nas casas e
        devolve o vencedor com base no total de sementes nos armazéns.
        """
        for idx, jogador in enumerate(self.jogadores):
            for casa in jogador.casas:
                sementes = casa.retirar_todas()
                for tipo_semente, quantidade in sementes.items():
                    if quantidade > 0:
                        jogador.armazem.adicionar_semente(tipo_semente, quantidade)
            
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
    
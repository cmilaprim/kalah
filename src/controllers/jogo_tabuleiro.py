import tkinter as tk
from typing import Optional
from models.tabuleiro import Tabuleiro
from views.interface_jogador import InterfaceJogador

class JogoTabuleiro:
    def __init__(self, root: tk.Tk):
        self.modelo = Tabuleiro()
        self.interface = InterfaceJogador(root, self)
        self.interface.receber_jogada(posicao=-1, 
                                    jogador=self.modelo.jogador_atual,
                                    estado_tabuleiro=self.modelo.estado_em_lista(), 
                                    armazens=self.modelo.armazens_em_lista())

    def jogada_valida(self, casa_index: int) -> bool:
        return self.modelo.jogada_valida(casa_index)

    def realizar_jogada(self, casa_index: int) -> None:
            if not self.jogada_valida(casa_index):
                return
            extra_turn = self.modelo.semear(casa_index)
            
            if self.modelo.jogo_terminou():
                vencedor = self.modelo.finalizar_jogo()
                if vencedor is None:
                    self.interface.informar_empate()  
                else:
                    self.interface.informar_vencedor(vencedor)
                return

            self.modelo.alternar_turno(extra_turn)
            self.interface.receber_jogada(posicao=casa_index,
                                        jogador=self.modelo.jogador_atual,
                                        estado_tabuleiro=self.modelo.estado_em_lista(),
                                        armazens=self.modelo.armazens_em_lista())
            
    def comecar_partida(self) -> None:
        self.modelo = Tabuleiro()
        self.interface.receber_jogada(
            posicao=-1,
            jogador=self.modelo.jogador_atual,
            estado_tabuleiro=self.modelo.estado_em_lista(),
            armazens=self.modelo.armazens_em_lista()
        )

    def recomecar_partida(self) -> None:
        self.comecar_partida()

    def jogo_terminou(self) -> bool:
        return self.modelo.jogo_terminou()
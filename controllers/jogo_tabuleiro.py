# controllers/jogo_tabuleiro.py

import tkinter as tk
from typing import Optional

from models.tabuleiro import Tabuleiro
from views.interface_jogador import InterfaceJogador


class JogoTabuleiro:
    def __init__(self, root: tk.Tk):
        self.modelo = Tabuleiro()
        self.interface = InterfaceJogador(root, self)
        self.interface.receive_move(posicao=-1, jogador=self.modelo.jogador_atual,estado_tabuleiro=self.modelo.estado_em_lista(), armazens=self.modelo.armazens_em_lista()        )

    def jogada_valida(self, casa_index: int) -> bool:
        return self.modelo.jogada_valida(casa_index)

    def realizar_jogada(self, casa_index: int) -> None:
        if not self.jogada_valida(casa_index):
            return
        extra_turn = self.modelo.semear(casa_index)
        if self.modelo.jogo_terminou():
            vencedor: Optional[int] = self.modelo.obter_vencedor()
            self.interface.inform_winner((vencedor) if vencedor is not None else 0)
            return

        self.modelo.alternar_turno(extra_turn)
        self.interface.receive_move(posicao=casa_index,jogador=self.modelo.jogador_atual,estado_tabuleiro=self.modelo.estado_em_lista(),armazens=self.modelo.armazens_em_lista())

    def reiniciar_jogo(self) -> None:
        self.modelo = Tabuleiro()
        self.interface.receive_move(posicao=-1,jogador=self.modelo.jogador_atual + 1,estado_tabuleiro=self.modelo.estado_em_lista(),armazens=self.modelo.armazens_em_lista())

    def jogo_terminou(self) -> bool:
        return self.modelo.jogo_terminou()

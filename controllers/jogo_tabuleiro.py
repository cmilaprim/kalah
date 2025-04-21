# controllers/jogo_tabuleiro.py

import tkinter as tk
from typing import Optional

from models.tabuleiro import Tabuleiro
from views.interface_jogador import InterfaceJogador


class JogoTabuleiro:
    def __init__(self, root: tk.Tk):
        self.modelo = Tabuleiro()
        #cria a view, injetando este controller
        self.interface = InterfaceJogador(root, self)
        #desenha o estado inicial
        self.interface.receive_move(
            posicao=-1,                             #nenhuma casa ficou marcada
            jogador=self.modelo.jogador_atual,
            estado_tabuleiro=self.modelo.estado_em_lista(),  #List[List[int]]
            armazens=self.modelo.armazens_em_lista()         #List[List[int]]
        )

    def jogada_valida(self, casa_index: int) -> bool:
        return self.modelo.jogada_valida(casa_index)

    def realizar_jogada(self, casa_index: int) -> None:
        if not self.jogada_valida(casa_index):
            return

        #faz toda a lógica de semeadura, captura e turno extra
        extra_turn = self.modelo.semear(casa_index)

        #se o jogo terminou, avisa o vencedor e sai
        if self.modelo.jogo_terminou():
            vencedor: Optional[int] = self.modelo.obter_vencedor()
            self.interface.inform_winner(
                (vencedor + 1) if vencedor is not None else 0
            )
            return

        #alterna turno se não for extra
        self.modelo.alternar_turno(extra_turn)

        #atualiza a view com o **novo** estado
        self.interface.receive_move(
            posicao=casa_index,
            jogador=self.modelo.jogador_atual,
            estado_tabuleiro=self.modelo.estado_em_lista(),
            armazens=self.modelo.armazens_em_lista()
        )

    def reiniciar_jogo(self) -> None:
        #reinicializa o modelo
        self.modelo = Tabuleiro()
        #desenha novamente o estado zerado
        self.interface.receive_move(
            posicao=-1,
            jogador=self.modelo.jogador_atual + 1,
            estado_tabuleiro=self.modelo.estado_em_lista(),
            armazens=self.modelo.armazens_em_lista()
        )

    def jogo_terminou(self) -> bool:
        #se a sua Interface chama self.controlador.jogo_terminou(),
        #basta repassar ao modelo:
        return self.modelo.jogo_terminou()

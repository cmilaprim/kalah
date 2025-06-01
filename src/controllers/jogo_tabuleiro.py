import tkinter as tk
from typing import Optional, Dict, Any
from models.tabuleiro import Tabuleiro
from views.interface_jogador import InterfaceJogador
from tkinter import messagebox

class JogoTabuleiro:
    def __init__(self, root: tk.Tk):
        self.modelo = Tabuleiro()
        self.interface = InterfaceJogador(root, self)
        self.jogador_local_id = None
        self.jogador_remoto_id = None
        self.minha_vez = False
        self.partida_iniciada = False
        self.dog_interface = None
        
        # Estado inicial do tabuleiro
        self.interface.receber_jogada(
            posicao=-1, 
            jogador=self.modelo.jogador_atual,
            estado_tabuleiro=self.modelo.estado_em_lista(), 
            armazens=self.modelo.armazens_em_lista()
        )

    def iniciar_partida(self, jogador_local_id, jogador_remoto_id, primeiro_jogador_id):
        """Inicia uma nova partida com os IDs dos jogadores"""
        self.jogador_local_id = str(jogador_local_id)
        self.jogador_remoto_id = str(jogador_remoto_id)
        self.primeiro_jogador_id = str(primeiro_jogador_id)
        
        # Determina se é a vez do jogador local
        self.minha_vez = (str(primeiro_jogador_id) == str(jogador_local_id))
        
        self.partida_iniciada = True
        self.modelo = Tabuleiro()
        self.interface.game_started = True
        
        # Configura a referência do dog_interface
        if hasattr(self.interface, 'dog_server_interface'):
            self.dog_interface = self.interface.dog_server_interface
        
        # Atualiza a interface
        self.interface.receber_jogada(
            posicao=-1,
            jogador=self.modelo.jogador_atual,
            estado_tabuleiro=self.modelo.estado_em_lista(),
            armazens=self.modelo.armazens_em_lista()
        )
        
        jogador_texto = "sua" if self.minha_vez else "do oponente"
        self.interface.status_label.config(text=f"Partida iniciada! Vez: {jogador_texto}")

    def sincronizar_estado_inicial(self, primeiro_jogador_id: str) -> None:
        """Sincroniza o estado inicial quando recebe notificação do oponente"""
        self.primeiro_jogador_id = str(primeiro_jogador_id)
        self.minha_vez = (str(primeiro_jogador_id) == str(self.jogador_local_id))
        
        jogador_texto = "sua" if self.minha_vez else "do oponente"
        self.interface.status_label.config(text=f"Partida sincronizada! Vez: {jogador_texto}")
        
        self.interface.receber_jogada(
            posicao=-1,
            jogador=self.modelo.jogador_atual,
            estado_tabuleiro=self.modelo.estado_em_lista(),
            armazens=self.modelo.armazens_em_lista()
        )

    def jogada_valida(self, casa_index: int) -> bool:
        """Verifica se uma jogada é válida"""
        return self.modelo.jogada_valida(casa_index)
    
    def realizar_jogada(self, casa_index: int) -> None:
        """Realiza uma jogada local e envia para o oponente via Dog"""
        if not self.partida_iniciada:
            messagebox.showwarning("Atenção", "Partida não iniciada!")
            return
            
        if not self.minha_vez:
            messagebox.showwarning("Atenção", "Não é sua vez de jogar!")
            return
            
        if not self.jogada_valida(casa_index):
            messagebox.showwarning("Atenção", "Jogada inválida!")
            return
        
        extra_turn = self.modelo.semear(casa_index)
        
        # Envia a jogada via Dog
        self.enviar_jogada_dog(casa_index)
        
        if self.modelo.jogo_terminou():
            vencedor = self.modelo.finalizar_jogo()
            self.finalizar_partida(vencedor)
            return

        # Atualiza o turno
        if not extra_turn:
            self.minha_vez = False
            self.modelo.alternar_turno(extra_turn)
            jogador_texto = "do oponente"
        else:
            jogador_texto = "sua (turno extra)"
            
        # Atualiza a interface
        self.interface.status_label.config(text=f"Vez: {jogador_texto}")
        self.interface.receber_jogada(
            posicao=casa_index,
            jogador=self.modelo.jogador_atual,
            estado_tabuleiro=self.modelo.estado_em_lista(),
            armazens=self.modelo.armazens_em_lista()
        )
        
    def enviar_jogada_dog(self, casa_index: int) -> None:
        """Envia a jogada para o oponente via Dog"""
        if not self.dog_interface:
            return
                
        dados_jogada = {
            'tipo': 'jogada',
            'casa_index': casa_index,
            'jogador': self.jogador_local_id,
            'match_status': 'finished' if self.modelo.jogo_terminou() else 'next'
        }
        
        try:
            self.dog_interface.send_move(dados_jogada)
        except Exception as e:
            print(f"Erro ao enviar jogada: {e}")
    
    def receber_jogada_remota(self, dados_jogada: Dict[str, Any]) -> None:
        """Recebe e processa uma jogada do oponente via Dog"""
        casa_index = dados_jogada.get('casa_index')
        
        # Executa a jogada
        extra_turn = self.modelo.semear(casa_index)
        
        if self.modelo.jogo_terminou():
            vencedor = self.modelo.finalizar_jogo()
            self.finalizar_partida(vencedor)
            return
        
        # Atualiza o turno
        if not extra_turn:
            self.minha_vez = True
            self.modelo.alternar_turno(extra_turn)
            jogador_texto = "sua"
        else:
            self.minha_vez = False
            jogador_texto = "do oponente (turno extra)"
        
        # Atualiza interface
        self.interface.status_label.config(text=f"Oponente jogou casa {casa_index}. Vez: {jogador_texto}")
        self.interface.receber_jogada(
            posicao=casa_index,
            jogador=self.modelo.jogador_atual,
            estado_tabuleiro=self.modelo.estado_em_lista(),
            armazens=self.modelo.armazens_em_lista()
        )
    
    def jogo_terminou(self) -> bool:
        """Verifica se o jogo terminou"""
        return self.modelo.jogo_terminou()

    def finalizar_partida(self, vencedor) -> None:
        """Finaliza a partida e informa o resultado"""
        self.partida_iniciada = False
        
        if vencedor is None:
            self.interface.informar_empate()
        else:
            nome_vencedor = "Você" if (
                (vencedor == 1 and str(self.jogador_local_id) == '1') or 
                (vencedor == 2 and str(self.jogador_local_id) == '2')
            ) else "Oponente"
            self.interface.informar_vencedor(nome_vencedor)

    def desistir_partida(self) -> None:
        """Desiste da partida atual"""
        if self.partida_iniciada and self.dog_interface:
            try:
                dados_jogada = {
                    'casa_index': -2,
                    'match_status': 'withdrawal',
                    'player': self.jogador_local_id
                }
                self.dog_interface.send_move(dados_jogada)
            except Exception as e:
                print(f"Erro ao notificar desistência: {e}")
                
        self.partida_iniciada = False
        self.interface.game_started = False

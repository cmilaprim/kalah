import tkinter as tk
from models.estado_partida import EstadoPartida
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
        self.interface.game_started = True
        
        # Atualiza a interface
        self.interface.receber_jogada(
            posicao=-1,
            jogador=self.modelo.jogador_atual,
            estado_tabuleiro=self.modelo.estado_em_lista(),
            armazens=self.modelo.armazens_em_lista()
        )
        
        jogador_texto = "sua" if self.minha_vez else "do oponente"
        self.interface.status_label.config(text=f"Partida iniciada! Vez: {jogador_texto}")

    def desistir_partida(self) -> None:
        """Desiste da partida atual"""
        if self.partida_iniciada:
            dados_desistencia = {
                'casa_index': -2,
                'match_status': 'withdrawal',
                'player': self.jogador_local_id
            }
            # CORRETO: Pede para Interface enviar
            self.interface.enviar_para_dog(dados_desistencia)
                
        self.partida_iniciada = False
        self.interface.game_started = False

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
    
    def realizar_jogada(self, casa_index: int) -> None:
        """Realiza uma jogada local e envia para o oponente via Interface"""
        # Validações já foram feitas em tentar_jogada, não precisa repetir
        
        # 1º PASSO: Atualização visual imediata (feedback responsivo)
        self.interface.status_label.config(text="Processando jogada...")
        
        # 2º PASSO: Executa a jogada completamente (semeadura + captura)
        extra_turn = self.modelo.semear(casa_index)
        
        # 3º PASSO: Atualiza a interface com o estado atual IMEDIATAMENTE
        self.interface.receber_jogada(
            posicao=casa_index,
            jogador=self.modelo.jogador_atual,
            estado_tabuleiro=self.modelo.estado_em_lista(),
            armazens=self.modelo.armazens_em_lista()
        )
        
        # 4º PASSO: Envia a jogada para o oponente de forma assíncrona
        self.interface.master.after(50, lambda: self.enviar_jogada_dog(casa_index))
        
        # 5º PASSO: Verifica se o jogo terminou com delay para visualização
        def verificar_e_finalizar():
            if self.modelo.jogo_terminou():
                # Mostra que está finalizando
                self.interface.status_label.config(text="Finalizando partida...")
                
                # Finaliza o jogo (coleta sementes restantes)
                vencedor = self.modelo.finalizar_jogo()
                
                # Atualiza interface final
                self.interface.receber_jogada(
                    posicao=-1,
                    jogador=self.modelo.jogador_atual,
                    estado_tabuleiro=self.modelo.estado_em_lista(),
                    armazens=self.modelo.armazens_em_lista()
                )
                
                # Mostra resultado final
                self.finalizar_partida(vencedor)
                return

            # Se o jogo continua, atualiza turnos
            if not extra_turn:
                self.minha_vez = False
                self.modelo.alternar_turno(extra_turn)
                jogador_texto = "do oponente"
            else:
                jogador_texto = "sua (turno extra)"
                
            self.interface.status_label.config(text=f"Vez: {jogador_texto}")
        
        self.interface.master.after(800, verificar_e_finalizar)

    def enviar_jogada_dog(self, casa_index: int) -> None:
        """Prepara dados e pede para Interface enviar via Dog"""
        # Verifica o estado APÓS a jogada ter sido processada
        jogo_acabou = self.modelo.jogo_terminou()
        
        dados_jogada = {
            'tipo': 'jogada',
            'casa_index': casa_index,
            'jogador': self.jogador_local_id,
            'match_status': 'finished' if jogo_acabou else 'next'
        }
        
        self.interface.enviar_para_dog(dados_jogada)
    
    def receber_jogada_remota(self, dados_jogada: Dict[str, Any]) -> None:
        """Recebe e processa uma jogada do oponente"""
        casa_index = dados_jogada.get('casa_index')
        extra_turn = self.modelo.semear(casa_index)
        
        self.interface.receber_jogada(
            posicao=casa_index,
            jogador=self.modelo.jogador_atual,
            estado_tabuleiro=self.modelo.estado_em_lista(),
            armazens=self.modelo.armazens_em_lista()
        )
        
        # Verifica fim de jogo com delay para visualização
        def verificar_e_finalizar_remoto():
            if self.modelo.jogo_terminou():
                # Mostra que está finalizando
                self.interface.status_label.config(text="Finalizando partida...")
                
                vencedor = self.modelo.finalizar_jogo()
                
                # Atualiza interface final
                self.interface.receber_jogada(
                    posicao=-1,
                    jogador=self.modelo.jogador_atual,
                    estado_tabuleiro=self.modelo.estado_em_lista(),
                    armazens=self.modelo.armazens_em_lista()
                )
                
                self.finalizar_partida(vencedor)
                return
            
            # Atualiza turnos normalmente
            if not extra_turn:
                self.minha_vez = True
                self.modelo.alternar_turno(extra_turn)
                jogador_texto = "sua"
            else:
                self.minha_vez = False
                jogador_texto = "do oponente (turno extra)"
            
            self.interface.status_label.config(text=f"Vez: {jogador_texto}")
        
        self.interface.master.after(800, verificar_e_finalizar_remoto)
    
    def jogo_terminou(self) -> bool:
        """Verifica se o jogo terminou"""
        return self.modelo.jogo_terminou()

    def finalizar_partida(self, vencedor) -> None:
        """Finaliza a partida e informa o resultado com contagem detalhada"""
        self.partida_iniciada = False
        
        sementes_j1 = self.modelo.jogadores[0].armazem.contar()
        sementes_j2 = self.modelo.jogadores[1].armazem.contar()
        
        if vencedor is None:
            self.interface.informar_empate(sementes_j1, sementes_j2)
        else:
            eh_jogador_1 = (str(self.primeiro_jogador_id) == str(self.jogador_local_id))
            
            if eh_jogador_1:
                nome_vencedor = "Você" if vencedor == 1 else "Oponente"
                suas_sementes = sementes_j1
                sementes_oponente = sementes_j2
            else:
                nome_vencedor = "Você" if vencedor == 2 else "Oponente"
                suas_sementes = sementes_j2
                sementes_oponente = sementes_j1
                
            self.interface.informar_vencedor(nome_vencedor, suas_sementes, sementes_oponente)

    
    def tentar_jogada(self, casa_index: int) -> dict:
        """Tenta realizar uma jogada e retorna o resultado"""
        # Validações rápidas primeiro
        if not self.partida_iniciada:
            return {
                'sucesso': False,
                'mensagem': 'Partida não iniciada!'
            }
        
        if not self.minha_vez:
            return {
                'sucesso': False,
                'mensagem': 'Não é sua vez!'
            }
        
        if not self.modelo.jogada_valida(casa_index):
            return {
                'sucesso': False,
                'mensagem': 'Jogada inválida!'
            }
        
        # Se chegou aqui, a jogada é válida - executa imediatamente
        self.realizar_jogada(casa_index)
        return {
            'sucesso': True,
            'mensagem': 'Jogada realizada com sucesso!'
        }
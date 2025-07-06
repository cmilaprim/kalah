import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
import math
from typing import List, Any

class InterfaceJogador(ttk.Frame, DogPlayerInterface):
    
    def __init__(self, master: tk.Tk, controlador: Any) -> None:
        style = ttk.Style()
        style.configure('My.TFrame', background='#F7F3E8')
        super().__init__(master, style='My.TFrame')

        self.master = master
        self.controlador = controlador
        self.game_started = False
        self.tabuleiro_width = 700  
        self.tabuleiro_height = 400  
        self.raio_casas = self.tabuleiro_width * 0.055  
        self.espaco_centro_casas = self.tabuleiro_width * 0.12 
        
        
        self.estado_tabuleiro: List[List[int]] = []
        self.armazens: List[List[int]] = []

        self.cores = {
            'fundo': "#F7F3E8",
            'tabuleiro': "#8B4513",
            'borda_tabuleiro': "#5D3A1A",
            'casas': "#E6D2B5",
            'sementes': '#A47551',
            'texto_botoes': '#FFFFFF',
            'botao_desistir': '#FF0000',
        }
        
        self.inicializar_janela()
        self.criar_status_frame()
        self.criar_canvas()
        self.criar_botao_desistir()

        player_name = simpledialog.askstring(title="Player Identification", prompt="Qual o seu nome?", parent=self.master)
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name, self)
        messagebox.showinfo("Conexão Dog", message, parent=self.master)

    def inicializar_janela(self) -> None:
        self.master.configure(bg='#F7F3E8')
        self.master.title("Tabuleiro de Kalah")
        
        largura_janela = 800  # Reduzido de 1100 para 800
        altura_janela = 550   # Reduzido de 700 para 550
        
        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()
        
        pos_x = (largura_tela // 2) - (largura_janela // 2)
        pos_y = (altura_tela // 2) - (altura_janela // 2)
        
        self.master.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
        
        self.pack(fill=tk.BOTH, expand=True)
        self.create_menu()

    def criar_status_frame(self) -> None:
        self.status_frame = tk.Frame(self, bg=self.cores['fundo'], height=50)
        self.status_frame.pack(fill=tk.X, side=tk.TOP)
        self.status_label = tk.Label(self.status_frame, text="Aguardando conexão...", font=("Helvetica", 16), bg=self.cores['fundo'], fg="#5C4033")
        self.status_label.pack(pady=10)
        
    def criar_canvas(self) -> None:
        self.canvas = tk.Canvas(self, width=self.tabuleiro_width, height=self.tabuleiro_height, bg=self.cores['tabuleiro'], highlightthickness=0)
        self.canvas.pack(padx=20, pady=(20, 10))
        self.canvas.bind("<Button-1>", self.click)

    def criar_botao_desistir(self) -> None:
        self.frame_botao = tk.Frame(self, bg=self.cores['fundo'])
        self.frame_botao.pack(fill=tk.X, pady=(10, 20))
        
        # Botão Desistir
        self.btn_desistir = tk.Button(
            self.frame_botao, 
            text="DESISTIR", 
            font=("Helvetica", 14, "bold"), 
            bg=self.cores['botao_desistir'], 
            fg=self.cores['texto_botoes'], 
            command=self.desistir, 
            width=12, 
            padx=12, 
            pady=5
        )
        self.btn_desistir.pack(anchor='center')
        
        # Botão Reiniciar (inicialmente oculto)
        self.btn_reiniciar = tk.Button(
            self.frame_botao,
            text="REINICIAR TABULEIRO",
            font=("Helvetica", 14, "bold"),
            bg="#006400",  # Verde escuro
            fg=self.cores['texto_botoes'],
            command=self.reiniciar_jogo,
            width=18,
            padx=12,
            pady=5
        )
        # Não faz pack() ainda - será mostrado apenas quando o jogo terminar

    def create_menu(self) -> None:
        menu_bar = tk.Menu(self.master)
        menu_opcoes = tk.Menu(menu_bar, tearoff=0)
        menu_opcoes.add_command(label="Iniciar Partida", command=self.start_match)
        menu_opcoes.add_separator()
        menu_opcoes.add_command(label="Reiniciar Tabuleiro", command=self.reiniciar_jogo_menu)
        menu_opcoes.add_separator()
        menu_opcoes.add_command(label="Regras do Jogo", command=self.mostrar_regras)
        menu_opcoes.add_separator()
        menu_opcoes.add_command(label="Sair", command=self.master.quit)
        menu_bar.add_cascade(label="Menu", menu=menu_opcoes)
        self.master.config(menu=menu_bar)

    def reiniciar_jogo_menu(self):
        """Método específico para reiniciar via menu"""
        # Chama diretamente o método normal
        self.reiniciar_jogo()

    def start_match(self):
        """Inicia uma partida usando o sistema Dog"""
        # Verifica se já há uma partida em andamento
        if (hasattr(self.controlador, 'partida_iniciada') and 
            self.controlador.partida_iniciada and 
            self.game_started):
            
            # Garante que a janela principal está em foco
            self.master.focus_force()
            self.master.lift()
            
            messagebox.showwarning(
                "Partida em Andamento", 
                "Já existe uma partida em andamento!\n\n"
                "Para iniciar uma nova partida:\n"
                "• Termine a partida atual jogando\n"
                "• Ou use o botão 'DESISTIR' para encerrar\n\n"
                "Não é possível iniciar múltiplas partidas.", 
                parent=self.master
            )
            return
        
        if not hasattr(self, 'dog_server_interface'):
            messagebox.showerror("Erro", "Conexão com servidor Dog não estabelecida.", parent=self.master)
            return
            
        start_status = self.dog_server_interface.start_match(2)
        message = start_status.get_message()
        messagebox.showinfo("Solicitação de Partida", message, parent=self.master)

    def receive_start(self, start_status):
        """Recebe a notificação de início de partida do Dog"""
        try:
            message = start_status.get_message()
            jogador_local_id = start_status.get_local_id()
            players = start_status.get_players()
            
            # Encontra o oponente e determina quem começa
            jogador_remoto_id = None
            primeiro_jogador_id = None
            
            for player_data in players:
                if isinstance(player_data, list) and len(player_data) >= 3:
                    player_id = player_data[1]
                    player_order = player_data[2]
                    
                    if player_id != str(jogador_local_id):
                        jogador_remoto_id = player_id
                    
                    if player_order == '1':
                        primeiro_jogador_id = player_id
            
            # Configura a partida
            self.game_started = True
            self.controlador.iniciar_partida(str(jogador_local_id), jogador_remoto_id, primeiro_jogador_id)
            
            # Esconde botão de reiniciar e mostra o de desistir
            self.esconder_botao_reiniciar()
            
            # Envia sincronização inicial
            self.master.after(2000, lambda: self.enviar_sincronizacao_inicial(primeiro_jogador_id))
            
            comeca = "Você começa!" if primeiro_jogador_id == str(jogador_local_id) else "Oponente começa!"
            
            # Força a janela principal para frente antes de mostrar o diálogo
            self.master.focus_force()
            self.master.lift()
            self.master.update_idletasks()
            messagebox.showinfo("Partida Iniciada", f"{message}\n\n{comeca}", parent=self.master)
            # Força o foco na janela principal após o diálogo
            self.master.focus_force()
            self.master.lift()
            
        except Exception as e:
            print(f"Erro ao processar início: {e}")
            messagebox.showwarning("Erro", f"Erro ao iniciar partida: {e}", parent=self.master)
    
    def enviar_para_dog(self, dados):
        """Envia dados para o servidor Dog"""
        if hasattr(self, 'dog_server_interface') and self.dog_server_interface:
            self.dog_server_interface.send_move(dados)
        else:
            print(f"Erro: Não foi possível enviar dados {dados} - conexão Dog indisponível")

    def enviar_sincronizacao_inicial(self, primeiro_jogador_id):
        """Envia mensagem de sincronização inicial"""
        dados_sync = {
            'tipo': 'sync_inicial',
            'primeiro_jogador': primeiro_jogador_id,
            'match_status': 'next'
        }
        self.dog_server_interface.send_move(dados_sync)

    def configurar_partida_via_sync(self, sync_data, primeiro_jogador):
        """Configura a partida via sincronização quando receive_start falhou"""
        try:
            if hasattr(self, 'dog_server_interface') and hasattr(self.dog_server_interface, 'proxy'):
                meu_id = str(self.dog_server_interface.proxy.player_id)
                oponente_id = sync_data.get('player', 'unknown')
                
                self.game_started = True
                self.controlador.iniciar_partida(meu_id, oponente_id, primeiro_jogador)
                
                comeca = "Você começa!" if primeiro_jogador == meu_id else "Oponente começa!"
                
                # Força a janela principal para frente antes de mostrar o diálogo
                self.master.focus_force()
                self.master.lift()
                self.master.update_idletasks()
                messagebox.showinfo("Partida Iniciada", f"Partida sincronizada!\n\n{comeca}", parent=self.master)
                # Força o foco na janela principal após o diálogo
                self.master.focus_force()
                self.master.lift()
                
        except Exception as e:
            print(f"Erro na configuração via sync: {e}")

    def click(self, event) -> None:
        if not self.game_started:
            return
        
        # Previne duplo clique desabilitando temporariamente os cliques
        if hasattr(self, '_processando_clique') and self._processando_clique:
            return
            
        item = self.canvas.find_closest(event.x, event.y)
        for tag in self.canvas.gettags(item):
            if tag.startswith("casa_"):
                idx = int(tag.split("_", 1)[1])
                
                # Marca que está processando clique
                self._processando_clique = True
                
                # Processa jogada diretamente (integrado do _processar_jogada_async)
                def processar_jogada():
                    try:
                        resultado = self.controlador.tentar_jogada(idx)
                        
                        if not resultado['sucesso']:
                            # Mostra mensagem no status (integrado do _mostrar_mensagem_async)
                            self.status_label.config(text=f"{resultado['mensagem']}")
                            # Volta ao texto normal após 2 segundos (integrado do _restaurar_status)
                            def restaurar_status():
                                if hasattr(self.controlador, 'minha_vez') and self.controlador.partida_iniciada:
                                    jogador_texto = "sua" if self.controlador.minha_vez else "do oponente"
                                    self.status_label.config(text=f"Vez: {jogador_texto}")
                                else:
                                    self.status_label.config(text="Aguardando...")
                            self.master.after(2000, restaurar_status)
                            self.atualizar_interface()
                    finally:
                        # Reabilita cliques após um pequeno delay (integrado do _habilitar_cliques)
                        def habilitar_cliques():
                            self._processando_clique = False
                        self.master.after(100, habilitar_cliques)
                
                self.master.after(10, processar_jogada)
                return
    
    def mostrar_mensagem(self, msg: str) -> None:
        """Mostra uma mensagem para o usuário"""
        messagebox.showwarning("Atenção", msg, parent=self.master)
    
    def atualizar_interface(self) -> None:
        """Atualiza a interface do tabuleiro"""
        self.desenhar_tabuleiro()

    def receive_move(self, move_data):
        """Recebe uma jogada do outro jogador via Dog"""
        try:
            if not isinstance(move_data, dict):
                if isinstance(move_data, str):
                    import json
                    move_data = json.loads(move_data)
                else:
                    return
            
            # Tratar sincronização inicial
            if move_data.get('tipo') == 'sync_inicial':
                primeiro_jogador = move_data.get('primeiro_jogador')
                if not hasattr(self.controlador, 'jogador_local_id') or not self.controlador.jogador_local_id:
                    self.configurar_partida_via_sync(move_data, primeiro_jogador)
                else:
                    self.controlador.sincronizar_estado_inicial(primeiro_jogador)
                return
            
            # Tratar jogada normal
            if move_data.get('tipo') == 'jogada':
                casa_index = move_data.get('casa_index')
                if getattr(self.controlador, 'partida_iniciada', False):
                    self.controlador.receber_jogada_remota({'casa_index': casa_index})
                return
            
            # Comandos especiais
            casa_index = move_data.get('casa_index')
            match_status = move_data.get('match_status')
            
            # Tratar desistência via casa_index especial
            if casa_index == -2 or match_status == 'withdrawal':
                self.processar_desistencia_oponente()
                return
                
            # Tratar interrupção (desistência detectada pelo servidor)
            if match_status == 'interrupted':
                self.processar_desistencia_oponente()
                return
                
        except Exception as e:
            print(f"Erro ao processar movimento: {e}")

    def processar_desistencia_oponente(self):
        """Processa desistência do oponente"""
        self.game_started = False
        self.controlador.partida_iniciada = False
        self.status_label.config(text="Oponente desistiu - Você venceu!")
        
        # Mostra botão de reiniciar
        self.mostrar_botao_reiniciar()
        
        messagebox.showinfo("Vitória!", "O oponente desistiu da partida.\nVocê venceu!", parent=self.master)

    def receive_withdrawal_notification(self):
        """Recebe notificação que o oponente abandonou a partida"""
        self.processar_desistencia_oponente()

    def receber_jogada(self, posicao: int, jogador: int, estado_tabuleiro: List[List[int]], armazens: List[List[int]]) -> None:
        """Atualiza a interface após uma jogada"""
        self.estado_tabuleiro = estado_tabuleiro
        self.armazens = armazens
        self.desenhar_tabuleiro()
        
        if self.controlador.partida_iniciada and hasattr(self.controlador, 'minha_vez'):
            jogador_texto = "sua" if self.controlador.minha_vez else "do oponente"
            self.status_label.config(text=f"Vez: {jogador_texto}")
        else:
            self.status_label.config(text=f"Vez do Jogador {jogador}")

    def desenhar_tabuleiro(self) -> None:
        self.canvas.delete("all")
        prop = 0.5
        y_topo = self.tabuleiro_height * (1 - prop) / 2
        y_base = self.tabuleiro_height * (1 + prop) / 2

        self.canvas.create_text(self.tabuleiro_width/2, self.tabuleiro_height*0.02, text="Casas do jogador 1", font=("Helvetica", 12), fill=self.cores['texto_botoes'])
        self.canvas.create_text(self.tabuleiro_width/2, self.tabuleiro_height*0.98, text="Casas do jogador 2", font=("Helvetica", 12), fill=self.cores['texto_botoes'])

        x_start = (self.tabuleiro_width - 5*self.espaco_centro_casas)/2

        for idx, quantidade_lista in enumerate(self.estado_tabuleiro):
            row = 0 if idx < 6 else 1
            col = idx if row == 0 else idx - 6
            x = x_start + col*self.espaco_centro_casas
            y = y_topo if row == 0 else y_base

            # Cria a casa
            self.canvas.create_oval(x-self.raio_casas, y-self.raio_casas, x+self.raio_casas, y+self.raio_casas, fill=self.cores['casas'], outline=self.cores['borda_tabuleiro'], width=4, tags=(f"casa_{idx}",))

            quantidade = quantidade_lista[0] 
            
            if quantidade > 0:
                seed_r = 8  # Reduzido de 10 para 8
                sementes_para_mostrar = min(quantidade, 12)
                
                for i in range(sementes_para_mostrar):
                    ang = math.radians(i * (360/sementes_para_mostrar))
                    rx = x + self.raio_casas*0.45*math.cos(ang)
                    ry = y + self.raio_casas*0.45*math.sin(ang)
                    self.canvas.create_oval(rx-seed_r, ry-seed_r, rx+seed_r, ry+seed_r, fill=self.cores['sementes'], outline="")
                    
            self.canvas.create_text(x, y, text=str(quantidade), font=("Helvetica", 12, "bold"), fill=self.cores['texto_botoes'])

        # Armazém J1 (esquerda)
        self.canvas.create_rectangle(15, y_topo, 80, y_base, fill=self.cores['casas'], outline=self.cores['borda_tabuleiro'], width=3)
        self.canvas.create_text(47.5, (y_topo + y_base)/2, text=str(self.armazens[0][0]), font=("Helvetica", 14, "bold"), fill=self.cores['texto_botoes'])
        self.canvas.create_text(47.5, y_base + 15, text="Armazém J1", font=("Helvetica", 10), fill=self.cores['texto_botoes'])

        # Armazém J2 (direita)
        warehouse_width = 65  
        warehouse_margin = 15 
        x2 = self.tabuleiro_width - warehouse_margin
        x1 = x2 - warehouse_width

        self.canvas.create_rectangle(x1, y_topo, x2, y_base, fill=self.cores['casas'], outline=self.cores['borda_tabuleiro'], width=3)
        cx = (x1 + x2)/2
        self.canvas.create_text(cx, (y_topo + y_base)/2, text=str(self.armazens[1][0]), font=("Helvetica", 14, "bold"), fill=self.cores['texto_botoes'])
        self.canvas.create_text(cx, y_base + 15, text="Armazém J2", font=("Helvetica", 10), fill=self.cores['texto_botoes'])

    def informar_vencedor(self, vencedor: str, suas_sementes: int, sementes_oponente: int) -> None:
        """Informa o vencedor da partida com delay para mostrar estado final"""
        def mostrar_resultado():
            mensagem = (f"PARTIDA FINALIZADA\n\n"
                    f"Vencedor: {vencedor}!\n\n"
                    f"CONTAGEM FINAL:\n"
                    f"•Suas sementes: {suas_sementes}\n"
                    f"•Sementes do oponente: {sementes_oponente}")
            
            # Garante que a janela principal está em foco
            self.master.focus_force()
            self.master.lift()
            
            messagebox.showinfo("Fim de Jogo", mensagem, parent=self.master)
            self.game_started = False
            self.status_label.config(text=f"Partida finalizada - Vencedor: {vencedor}")
            
            # Mostra botão de reiniciar
            self.mostrar_botao_reiniciar()
        
        # Aguarda 1 segundo para mostrar o resultado (tempo para ver o estado final)
        self.master.after(1000, mostrar_resultado)
        
        
    def informar_empate(self, sementes_j1: int, sementes_j2: int) -> None:
        """Informa empate com delay para mostrar estado final"""
        def mostrar_resultado():
            mensagem = (f"PARTIDA FINALIZADA\n\n"
                    f"EMPATE!\n\n"
                    f"CONTAGEM FINAL:\n"
                    f"•Jogador 1: {sementes_j1} sementes\n"
                    f"•Jogador 2: {sementes_j2} sementes\n\n"
                    f"Ambos têm o mesmo número de sementes!")
            
            # Garante que a janela principal está em foco
            self.master.focus_force()
            self.master.lift()
            
            messagebox.showinfo("Fim de Jogo", mensagem, parent=self.master)
            self.game_started = False
            self.status_label.config(text="Partida finalizada - Empate")
            
            # Mostra botão de reiniciar
            self.mostrar_botao_reiniciar()
        
        self.master.after(1000, mostrar_resultado)

    def desistir(self):
        """Desiste da partida atual"""
        if not self.game_started:
            messagebox.showinfo("Atenção", "Nenhuma partida em andamento.", parent=self.master)
            return
        
        # Garante que a janela principal está em foco
        self.master.focus_force()
        self.master.lift()
        
        resposta = messagebox.askyesno(
            "Confirmar Desistência", 
            "Tem certeza que deseja desistir da partida?\n\nIsso contará como derrota.", 
            parent=self.master
        )
        
        if resposta:
            # Tenta desistir via controlador
            sucesso = False
            if hasattr(self.controlador, 'desistir_partida'):
                sucesso = self.controlador.desistir_partida()
            
            if sucesso:
                messagebox.showinfo("Desistência", "Você desistiu da partida.", parent=self.master)
            else:
                # Fallback - força finalização local se houver erro
                self.game_started = False
                self.status_label.config(text="Partida encerrada (desistência)")
                messagebox.showwarning("Aviso", "Houve um problema ao comunicar a desistência, mas a partida foi encerrada localmente.", parent=self.master)

    def mostrar_regras(self) -> None:
        regras = (
            "Regras do Kalah:\n"
            "1. O jogo começa com 4 sementes em cada buraco.\n"
            "2. No seu turno, escolha um buraco do seu lado para coletar todas as sementes.\n"
            "3. Distribua as sementes no sentido anti-horário, pulando o armazém adversário.\n"
            "4. Se a última semente cair em um buraco vazio do seu lado e o oposto tiver sementes, capture-as.\n"
            "5. Se cair no seu armazém, joga de novo.\n"
            "6. Termina quando um lado esvaziar.\n"
            "7. Quem tiver mais sementes vence."
        )
        messagebox.showinfo("Regras do Jogo", regras, parent=self.master)

    def reiniciar_jogo(self):
        """Reinicia o tabuleiro para o estado inicial - reset simples"""
        
        # Mensagem de confirmação
        # Garante que a janela principal está em foco
        self.master.focus_force()
        self.master.lift()
        
        resposta = messagebox.askyesno(
            "Reiniciar Tabuleiro", 
            "Tem certeza que deseja reiniciar o tabuleiro?\n\n"
            "O tabuleiro voltará ao estado inicial (4 sementes por casa).\n"
            "Para jogar novamente, use 'Menu → Iniciar Partida'.\n\n"
            "Continuar?", 
            parent=self.master
        )
        
        if resposta:
            # Chama o método do controlador
            sucesso = False
            if hasattr(self.controlador, 'reiniciar_jogo'):
                sucesso = self.controlador.reiniciar_jogo()
            
            if sucesso:
                # Esconde o botão reiniciar e mostra o desistir centralizado
                self.btn_reiniciar.pack_forget()
                self.btn_desistir.pack(anchor='center')
                
                messagebox.showinfo(
                    "Tabuleiro Reiniciado", 
                    "Tabuleiro reiniciado com sucesso!\n\n"
                    "Estado inicial restaurado.\n"
                    "Use 'Menu → Iniciar Partida' para uma nova partida.", 
                    parent=self.master
                )
            else:
                messagebox.showerror("Erro", "Não foi possível reiniciar o tabuleiro.", parent=self.master)

    def mostrar_botao_reiniciar(self):
        """Mostra o botão de reiniciar e esconde o de desistir"""
        self.btn_desistir.pack_forget()
        self.btn_reiniciar.pack(anchor='center')

    def esconder_botao_reiniciar(self):
        """Esconde o botão de reiniciar e mostra o de desistir"""
        self.btn_reiniciar.pack_forget()
        self.btn_desistir.pack(anchor='center')

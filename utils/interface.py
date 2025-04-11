import tkinter as tk
from tkinter import messagebox, Menu
import math
import random

class KalahBoard:
    def __init__(self, master):
        self.master = master
        master.title("Tabuleiro de Kalah")
        
        self.largura_tabuleiro = 1200
        self.altura_tabuleiro = 600
        self.raio_buracos = self.largura_tabuleiro * 0.05
        self.espaco_centro_buracos = self.largura_tabuleiro * 0.13
        
        # Estado do jogo
        self.jogador_atual = 1
        self.estado_jogo = [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]]  # Sementes em cada buraco
        self.pontuacao = [0, 0]  # Pontuação dos jogadores
        
        # Criar o menu
        self.criar_menu()
        
        # Frame principal que conterá o tabuleiro e o painel de informações
        self.frame_principal = tk.Frame(master)
        self.frame_principal.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Frame para informações e estatísticas
        self.frame_info = tk.Frame(self.frame_principal, bg='wheat', bd=2, relief=tk.RAISED)
        self.frame_info.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        # Exibir informações do jogo
        self.label_turno = tk.Label(self.frame_info, text=f"Turno: Jogador {self.jogador_atual}",font=("Arial", 14, "bold"), bg='wheat')
        self.label_turno.pack(side=tk.LEFT, padx=20)
        
        self.label_pontuacao1 = tk.Label(self.frame_info, text=f"Jogador 1: {self.pontuacao[0]}", font=("Arial", 14), bg='wheat')
        self.label_pontuacao1.pack(side=tk.LEFT, padx=20)
        
        self.label_pontuacao2 = tk.Label(self.frame_info, text=f"Jogador 2: {self.pontuacao[1]}", font=("Arial", 14), bg='wheat')
        self.label_pontuacao2.pack(side=tk.LEFT, padx=20)
        
        # Botão para reiniciar o jogo
        self.botao_reiniciar = tk.Button(self.frame_info, text="Reiniciar Jogo", command=self.reiniciar_jogo, font=("Arial", 12), bg='lightblue')
        self.botao_reiniciar.pack(side=tk.RIGHT, padx=20)
        
        # Canvas para o tabuleiro
        self.tabuleiro = tk.Canvas(self.frame_principal, width=self.largura_tabuleiro, height=self.altura_tabuleiro, bg='wheat')
        self.tabuleiro.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
        # Armazena referências para os elementos visuais
        self.buracos_elementos = [[], []]  # Lista para armazenar os IDs dos buracos
        self.sementes_elementos = [[], []]  # Lista para armazenar os IDs das sementes
        self.textos_contagem = [[], []]  # Lista para armazenar os textos de contagem
        
        self.centraliza_tela()
        self.desenha_tabuleiro()
        
    def criar_menu(self):
        menu_bar = Menu(self.master)
        self.master.config(menu=menu_bar)
        
        # Menu Arquivo
        arquivo_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Arquivo", menu=arquivo_menu)
        arquivo_menu.add_command(label="Novo Jogo", command=self.reiniciar_jogo)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="Sair", command=self.master.quit)
        
        # Menu Ajuda
        ajuda_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Ajuda", menu=ajuda_menu)
        ajuda_menu.add_command(label="Regras do Jogo", command=self.mostrar_regras)
        ajuda_menu.add_command(label="Sobre", command=self.mostrar_sobre)
    
    def mostrar_regras(self):
        regras = """Regras do Kalah:
1. O jogo começa com 4 sementes em cada buraco.
2. No seu turno, escolha um buraco do seu lado para coletar todas as sementes.
3. Distribua as sementes no sentido anti-horário, uma em cada buraco.
4. Se a última semente cair em um buraco vazio do seu lado, capture essa semente e todas as sementes do buraco oposto.
5. Se a última semente cair no seu armazém, você ganha um turno extra.
6. O jogo termina quando todos os buracos de um lado estiverem vazios.
7. O jogador com mais sementes no final vence."""
        messagebox.showinfo("Regras do Kalah", regras)
    
    def mostrar_sobre(self):
        messagebox.showinfo("Sobre Kalah", "Jogo Kalah v1.0\nDesenvolvido como exemplo para melhoria de interface com Tkinter")
    
    def reiniciar_jogo(self):
        # Reiniciar o estado do jogo
        self.jogador_atual = 1
        self.estado_jogo = [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]]
        self.pontuacao = [0, 0]
        
        # Atualizar informações
        self.atualizar_informacoes()
        
        # Redesenhar o tabuleiro
        self.tabuleiro.delete("all")
        self.desenha_tabuleiro()
        
    def atualizar_informacoes(self):
        self.label_turno.config(text=f"Turno: Jogador {self.jogador_atual}")
        self.label_pontuacao1.config(text=f"Jogador 1: {self.pontuacao[0]}")
        self.label_pontuacao2.config(text=f"Jogador 2: {self.pontuacao[1]}")
        
    def centraliza_tela(self):
        self.master.update_idletasks()
        largura_janela = self.master.winfo_width()
        altura_janela = self.master.winfo_height()
        largura_tela = self.master.winfo_screenwidth()
        altura_tela = self.master.winfo_screenheight()
        pos_x = (largura_tela - largura_janela) // 2
        pos_y = (altura_tela - altura_janela) // 2
        self.master.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
    
    def desenha_tabuleiro(self):
        self.tabuleiro.create_rectangle(0, 0, self.largura_tabuleiro, self.altura_tabuleiro, 
                                      fill='saddle brown', outline='brown')
        
        margem_horizontal = self.largura_tabuleiro * 0.01
        margem_vertical = self.altura_tabuleiro * 0.2
        largura_armazem = self.largura_tabuleiro * 0.10
        altura_armazem = self.altura_tabuleiro * 0.7
        x_inicio = (self.largura_tabuleiro - (5 * self.espaco_centro_buracos)) // 2
        
        centro_y = self.altura_tabuleiro / 2
        
        # Armazém 1
        armazem1 = self.tabuleiro.create_rectangle(margem_horizontal, margem_vertical, 
                                                 margem_horizontal + largura_armazem, 
                                                 margem_vertical + altura_armazem, 
                                                 fill='burlywood', outline='black', width=3)
        
        # Texto para armazém 1
        self.texto_armazem1 = self.tabuleiro.create_text(margem_horizontal + largura_armazem/2,
                                                       centro_y, text=str(self.pontuacao[0]), 
                                                       font=("Arial", 16, "bold"))
        
        # Armazém 2
        armazem2 = self.tabuleiro.create_rectangle(self.largura_tabuleiro - margem_horizontal - largura_armazem, 
                                                 margem_vertical, self.largura_tabuleiro - margem_horizontal, 
                                                 margem_vertical + altura_armazem, fill='burlywood', 
                                                 outline='black', width=3)
        
        # Texto para armazém 2
        self.texto_armazem2 = self.tabuleiro.create_text(self.largura_tabuleiro - margem_horizontal - largura_armazem/2,
                                                       centro_y, text=str(self.pontuacao[1]), 
                                                       font=("Arial", 16, "bold"))
        
        # Buracos
        y_topo = centro_y - self.altura_tabuleiro * 0.15
        y_base = centro_y + self.altura_tabuleiro * 0.15
        
        for i in range(6):
            x = x_inicio + i * self.espaco_centro_buracos
            
            # Buracos do topo (jogador 2)
            buraco_id = self.tabuleiro.create_oval(x - self.raio_buracos, y_topo - self.raio_buracos, 
                                                 x + self.raio_buracos, y_topo + self.raio_buracos, 
                                                 fill='burlywood', outline='black', width=3, 
                                                 tags=f"buraco_2_{5-i}")
            self.buracos_elementos[1].append(buraco_id)
            
            # Texto de contagem para o buraco do topo
            texto_id = self.tabuleiro.create_text(x, y_topo - self.raio_buracos - 15, 
                                                text=str(self.estado_jogo[1][5-i]), 
                                                font=("Arial", 12, "bold"))
            self.textos_contagem[1].append(texto_id)
            
            # Buracos da base (jogador 1)
            buraco_id = self.tabuleiro.create_oval(x - self.raio_buracos, y_base - self.raio_buracos, 
                                                 x + self.raio_buracos, y_base + self.raio_buracos, 
                                                 fill='burlywood', outline='black', width=3, 
                                                 tags=f"buraco_1_{i}")
            self.buracos_elementos[0].append(buraco_id)
            
            # Texto de contagem para o buraco da base
            texto_id = self.tabuleiro.create_text(x, y_base + self.raio_buracos + 15, 
                                                text=str(self.estado_jogo[0][i]), 
                                                font=("Arial", 12, "bold"))
            self.textos_contagem[0].append(texto_id)
            
            # Desenhar sementes
            self.desenha_sementes(x, y_topo, self.estado_jogo[1][5-i], 1, 5-i)
            self.desenha_sementes(x, y_base, self.estado_jogo[0][i], 0, i)
            
            # Adicionar eventos de clique para os buracos
            self.tabuleiro.tag_bind(f"buraco_1_{i}", "<Button-1>", lambda e, idx=i: self.clicar_buraco(0, idx))
            self.tabuleiro.tag_bind(f"buraco_2_{5-i}", "<Button-1>", lambda e, idx=5-i: self.clicar_buraco(1, idx))
        
        # Destacar o jogador atual
        self.destacar_jogador_atual()
    
    def desenha_sementes(self, x_centro, y_centro, num_sementes, jogador, indice):
        # Limpar sementes anteriores se houver
        if len(self.sementes_elementos) > jogador and len(self.sementes_elementos[jogador]) > indice:
            for semente_id in self.sementes_elementos[jogador][indice]:
                self.tabuleiro.delete(semente_id)
        
        # Garantir que há espaço suficiente na lista
        while len(self.sementes_elementos) <= jogador:
            self.sementes_elementos.append([])
        
        while len(self.sementes_elementos[jogador]) <= indice:
            self.sementes_elementos[jogador].append([])
        
        self.sementes_elementos[jogador][indice] = []
        
        if num_sementes == 0:
            return
        
        ball_radius = self.raio_buracos * 0.15
        
        # Determinar o layout das sementes com base na quantidade
        if num_sementes <= 6:
            # Circular para poucas sementes
            raio_circulo = self.raio_buracos * 0.5
            for i in range(num_sementes):
                angulo = i * (360 / num_sementes)
                ball_x = x_centro + raio_circulo * math.cos(math.radians(angulo))
                ball_y = y_centro + raio_circulo * math.sin(math.radians(angulo))
                
                # Usar cor diferente para cada jogador
                cor = 'royal blue' if jogador == 0 else 'crimson'
                
                semente_id = self.tabuleiro.create_oval(
                    ball_x - ball_radius, ball_y - ball_radius, 
                    ball_x + ball_radius, ball_y + ball_radius, 
                    fill=cor, outline='black', width=1
                )
                self.sementes_elementos[jogador][indice].append(semente_id)
        else:
            # Disposição pseudo-aleatória para muitas sementes
            for i in range(num_sementes):
                # Usar um raio menor para acomodar mais sementes
                raio_aleatorio = random.uniform(0, self.raio_buracos * 0.65)
                angulo_aleatorio = random.uniform(0, 360)
                
                ball_x = x_centro + raio_aleatorio * math.cos(math.radians(angulo_aleatorio))
                ball_y = y_centro + raio_aleatorio * math.sin(math.radians(angulo_aleatorio))
                
                # Usar cor diferente para cada jogador com variação leve
                r = random.randint(-20, 20)
                g = random.randint(-20, 20)
                b = random.randint(-20, 20)
                
                cor_base = 'royal blue' if jogador == 0 else 'crimson'
                cor = cor_base  # Simplificando, mantemos a cor base
                
                semente_id = self.tabuleiro.create_oval(
                    ball_x - ball_radius, ball_y - ball_radius, 
                    ball_x + ball_radius, ball_y + ball_radius, 
                    fill=cor, outline='black', width=1
                )
                self.sementes_elementos[jogador][indice].append(semente_id)
    
    def destacar_jogador_atual(self):
        # Destacar os buracos do jogador atual
        for jogador in [0, 1]:
            cor_borda = 'gold' if jogador == self.jogador_atual - 1 else 'black'
            espessura_borda = 5 if jogador == self.jogador_atual - 1 else 3
            
            for buraco_id in self.buracos_elementos[jogador]:
                self.tabuleiro.itemconfig(buraco_id, outline=cor_borda, width=espessura_borda)
    
    def clicar_buraco(self, jogador, indice):
        # Verificar se é o turno do jogador correto
        if jogador != self.jogador_atual - 1:
            messagebox.showinfo("Jogada Inválida", f"É a vez do Jogador {self.jogador_atual}!")
            return
        
        # Verificar se o buraco tem sementes
        if self.estado_jogo[jogador][indice] == 0:
            messagebox.showinfo("Jogada Inválida", "Este buraco está vazio!")
            return
        
        # Aqui você implementaria a lógica do jogo
        # Por enquanto, apenas simulamos uma jogada
        sementes = self.estado_jogo[jogador][indice]
        self.estado_jogo[jogador][indice] = 0
        
        # Simular distribuição de sementes (lógica simplificada)
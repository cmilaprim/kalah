import tkinter as tk
from tkinter import messagebox, Menu
import random
import math

class GameScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        self.CORES = {
            'fundo': "#F7F3E8", 
            'tabuleiro': "#8B4513", 
            'borda_tabuleiro': "#5D3A1A",  
            'buracos': "#E6D2B5",
            'sementes_jogador1': '#7D8C5B',  
            'sementes_jogador2': '#A47551',  
            'painel_info': '#F0E6D2', 
            'botoes': '#6B8E23', 
            'texto_botoes': '#FFFFFF'  
        }
        
        self.config_tabuleiro = {
            'largura': 1200,
            'altura': 700,
            'raio_buracos': 60,  
            'espaco_centro_buracos': 156, 
            'margem_horizontal': 12,
            'margem_vertical': 120,
        }
        
        self.jogador_atual = 1
        self.estado_jogo = [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]]  
        self.pontuacao = [0, 0]
        
        self.buracos_elementos = [[], []]  
        self.sementes_elementos = [[], []]  
        
        self.configure(bg=self.CORES['fundo'])
        self.inicializar_interface()
        
    def inicializar_interface(self):
        """cria todos os elementos da interface"""
        self.criar_layout_principal()
        self.criar_painel_informacoes()
        self.criar_tabuleiro()
        self.desenhar_tabuleiro()
        
    def criar_layout_principal(self):
        """cria o frame principal que contém todos os elementos"""
        self.frame_principal = tk.Frame(self, bg=self.CORES['fundo'])
        self.frame_principal.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
    def criar_painel_informacoes(self):
        """cria o painel superior com informações do jogo e botões"""
        self.frame_info = tk.Frame(self.frame_principal, bg=self.CORES['painel_info'], bd=2, relief=tk.RAISED)
        self.frame_info.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        
        # Labels de informação
        self.label_turno = tk.Label(self.frame_info, text=f"Turno: Jogador {self.jogador_atual}",
                                    font=("Arial", 14, "bold"), bg=self.CORES['painel_info'])
        self.label_turno.pack(side=tk.LEFT, padx=20)
        
        self.label_pontuacao1 = tk.Label(self.frame_info, text=f"Jogador 1: {self.pontuacao[0]}", 
                                        font=("Arial", 14), bg=self.CORES['painel_info'])
        self.label_pontuacao1.pack(side=tk.LEFT, padx=20)
        
        self.label_pontuacao2 = tk.Label(self.frame_info, text=f"Jogador 2: {self.pontuacao[1]}", 
                                        font=("Arial", 14), bg=self.CORES['painel_info'])
        self.label_pontuacao2.pack(side=tk.LEFT, padx=20)
        
        # Frame e botões
        self.criar_botoes()
    
    def criar_botoes(self):
        """cria os botões de controle do jogo"""
        frame_botoes = tk.Frame(self.frame_info, bg=self.CORES['painel_info'])
        frame_botoes.pack(side=tk.RIGHT, padx=10)
        
        self.botao_reiniciar = tk.Button(
            frame_botoes, 
            text="Reiniciar", 
            command=self.reiniciar_jogo, 
            font=("Arial", 12), 
            bg=self.CORES['botoes'], 
            fg=self.CORES['texto_botoes'],
            padx=10
        )
        self.botao_reiniciar.pack(side=tk.RIGHT, padx=5)
        
        self.botao_menu = tk.Button(frame_botoes, text="Menu Principal", command=lambda: self.controller.show_frame("StartScreen"), 
            font=("Arial", 12), 
            bg=self.CORES['botoes'], 
            fg=self.CORES['texto_botoes'],
            padx=10
        )
        self.botao_menu.pack(side=tk.RIGHT, padx=5)
        
        self.botao_regras = tk.Button(frame_botoes, text="Regras", command=self.mostrar_regras, 
            font=("Arial", 12), 
            bg=self.CORES['botoes'], 
            fg=self.CORES['texto_botoes'],
            padx=10
        )
        self.botao_regras.pack(side=tk.RIGHT, padx=5)
    
    def criar_tabuleiro(self):
        """cria o canvas do tabuleiro"""
        self.tabuleiro = tk.Canvas(
            self.frame_principal, 
            width=self.config_tabuleiro['largura'], 
            height=self.config_tabuleiro['altura'], 
            bg=self.CORES['tabuleiro']
        )
        self.tabuleiro.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
    
    def mostrar_regras(self):
        """exibe as regras do jogo em uma caixa de diálogo"""
        regras = """Regras do Kalah:
                1. O jogo começa com 4 sementes em cada buraco.
                2. No seu turno, escolha um buraco do seu lado para coletar todas as sementes.
                3. Distribua as sementes no sentido anti-horário, uma em cada buraco.
                4. Se a última semente cair em um buraco vazio do seu lado, capture essa semente e todas as sementes do buraco oposto.
                5. Se a última semente cair no seu armazém, você ganha um turno extra.
                6. O jogo termina quando todos os buracos de um lado estiverem vazios.
                7. O jogador com mais sementes no final vence."""
        messagebox.showinfo("Regras do Kalah", regras)
    
    def reiniciar_jogo(self):
        """reinicia o estado do jogo e atualiza a interface"""
        self.jogador_atual = 1
        self.estado_jogo = [[4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4]]
        self.pontuacao = [0, 0]
        
        self.atualizar_informacoes()
        self.tabuleiro.delete("all")
        self.desenhar_tabuleiro()
    
    def atualizar_informacoes(self):
        """atualiza as informações do jogo no painel superior"""
        self.label_turno.config(text=f"Turno: Jogador {self.jogador_atual}")
        self.label_pontuacao1.config(text=f"Jogador 1: {self.pontuacao[0]}")
        self.label_pontuacao2.config(text=f"Jogador 2: {self.pontuacao[1]}")
    
    def desenhar_tabuleiro(self):
        """desenha todos os elementos do tabuleiro"""
        self.desenhar_fundo_tabuleiro()
        self.desenhar_armazens()
        self.desenhar_buracos_e_sementes()
    
    def desenhar_fundo_tabuleiro(self):
        """desenha o fundo do tabuleiro"""
        self.tabuleiro.create_rectangle(0, 0, self.config_tabuleiro['largura'], 
                                        self.config_tabuleiro['altura'], 
                                        fill=self.CORES['tabuleiro'], 
                                        outline=self.CORES['borda_tabuleiro'], 
                                        width=3)
    
    def desenhar_armazens(self):
        """desenha os armazéns dos jogadores"""
        largura_armazem = self.config_tabuleiro['largura'] * 0.10
        altura_armazem = self.config_tabuleiro['altura'] * 0.7
        centro_y = self.config_tabuleiro['altura'] / 2
        
        self.armazem1 = self.tabuleiro.create_rectangle(
            self.config_tabuleiro['margem_horizontal'],
            self.config_tabuleiro['margem_vertical'], 
            self.config_tabuleiro['margem_horizontal'] + largura_armazem, 
            self.config_tabuleiro['margem_vertical'] + altura_armazem, 
            fill=self.CORES['buracos'], 
            outline='black', 
            width=3
        )
        
        self.texto_armazem1 = self.tabuleiro.create_text(self.config_tabuleiro['margem_horizontal'] + largura_armazem/2, centro_y, 
            text=str(self.pontuacao[0]), 
            font=("Arial", 16, "bold")
        )
        
        self.armazem2 = self.tabuleiro.create_rectangle(
            self.config_tabuleiro['largura'] - self.config_tabuleiro['margem_horizontal'] - largura_armazem,
            self.config_tabuleiro['margem_vertical'], 
            self.config_tabuleiro['largura'] - self.config_tabuleiro['margem_horizontal'], 
            self.config_tabuleiro['margem_vertical'] + altura_armazem, 
            fill=self.CORES['buracos'], 
            outline='black', 
            width=3
        )
        
        self.texto_armazem2 = self.tabuleiro.create_text(self.config_tabuleiro['largura'] - self.config_tabuleiro['margem_horizontal'] - largura_armazem/2,
            centro_y, 
            text=str(self.pontuacao[1]), 
            font=("Arial", 16, "bold")
        )
    
    def desenhar_buracos_e_sementes(self):
        """desenha os buracos e as sementes para ambos os jogadores"""
        centro_y = self.config_tabuleiro['altura'] / 2
        y_topo = centro_y - self.config_tabuleiro['altura'] * 0.15
        y_base = centro_y + self.config_tabuleiro['altura'] * 0.15
        
        #calculando a posição inicial para centralizar os buracos
        x_inicio = (self.config_tabuleiro['largura'] - (5 * self.config_tabuleiro['espaco_centro_buracos'])) // 2
        
        self.buracos_elementos = [[], []]
        self.sementes_elementos = [[], []]
        
        for i in range(6):
            x = x_inicio + i * self.config_tabuleiro['espaco_centro_buracos']
            
            #buracos do topo (jogador 2)
            self.desenhar_buraco(x, y_topo, 1, 5-i)
            
            #buracos da base (jogador 1)
            self.desenhar_buraco(x, y_base, 0, i)
    
    def desenhar_buraco(self, x, y, jogador, indice):
        """desenha um buraco específico e suas sementes"""
        buraco_id = self.tabuleiro.create_oval(
            x - self.config_tabuleiro['raio_buracos'], 
            y - self.config_tabuleiro['raio_buracos'], 
            x + self.config_tabuleiro['raio_buracos'], 
            y + self.config_tabuleiro['raio_buracos'], 
            fill=self.CORES['buracos'], 
            outline='black', 
            width=2, 
            tags=f"buraco_{jogador+1}_{indice}"
        )
        self.buracos_elementos[jogador].append(buraco_id)
        
        #desenhar sementes
        self.desenhar_sementes(x, y, self.estado_jogo[jogador][indice], jogador, indice)
    
    def desenhar_sementes(self, x_centro, y_centro, num_sementes, jogador, indice):
        """desenha as sementes em um buraco específico"""
        #limpar sementes anteriores se existirem
        if jogador < len(self.sementes_elementos) and indice < len(self.sementes_elementos[jogador]):
            for semente_id in self.sementes_elementos[jogador][indice]:
                self.tabuleiro.delete(semente_id)
        
        #garantir que temos espaço suficiente nas listas
        while len(self.sementes_elementos) <= jogador:
            self.sementes_elementos.append([])
            
        while len(self.sementes_elementos[jogador]) <= indice:
            self.sementes_elementos[jogador].append([])
        
        self.sementes_elementos[jogador][indice] = []
        
        if num_sementes == 0:
            return
            
        #tamanho das sementes
        raio_semente = self.config_tabuleiro['raio_buracos'] * 0.25
        
        #escolher a cor das sementes com base no jogador
        cor_semente = self.CORES['sementes_jogador1'] if jogador == 0 else self.CORES['sementes_jogador2']
        
        #estratégia de posicionamento baseada no número de sementes
        if num_sementes <= 8:
            self.desenhar_sementes_em_circulo(x_centro, y_centro, num_sementes, raio_semente, cor_semente, jogador, indice)
        else:
            self.desenhar_sementes_aleatorias(x_centro, y_centro, num_sementes, raio_semente, cor_semente, jogador, indice)
    
    def desenhar_sementes_em_circulo(self, x, y, quantidade, raio_semente, cor, jogador, indice):
        """desenha sementes em um padrão circular"""
        raio_circulo = self.config_tabuleiro['raio_buracos'] * 0.5
        for i in range(quantidade):
            angulo = i * (360 / quantidade)
            semente_x = x + raio_circulo * math.cos(math.radians(angulo))
            semente_y = y + raio_circulo * math.sin(math.radians(angulo))
            
            semente_id = self.tabuleiro.create_oval(
                semente_x - raio_semente, semente_y - raio_semente,
                semente_x + raio_semente, semente_y + raio_semente,
                fill=cor, outline='black', width=1
            )
            self.sementes_elementos[jogador][indice].append(semente_id)
    
    def desenhar_sementes_aleatorias(self, x, y, quantidade, raio_semente, cor, jogador, indice):
        """desenha sementes em posições aleatórias dentro do buraco"""
        for _ in range(quantidade):
            #usar um raio menor para evitar ultrapassar os limites do buraco
            raio_aleatorio = random.uniform(0, self.config_tabuleiro['raio_buracos'] * 0.7)
            angulo_aleatorio = random.uniform(0, 360)
            
            semente_x = x + raio_aleatorio * math.cos(math.radians(angulo_aleatorio))
            semente_y = y + raio_aleatorio * math.sin(math.radians(angulo_aleatorio))
            
            semente_id = self.tabuleiro.create_oval(
                semente_x - raio_semente, semente_y - raio_semente,
                semente_x + raio_semente, semente_y + raio_semente,
                fill=cor, outline='black', width=1
            )
            self.sementes_elementos[jogador][indice].append(semente_id)
            
    def redimensionar(self, largura, altura):
        """ajusta o tamanho do tabuleiro quando a janela é redimensionada"""

        nova_largura = largura - 40  
        nova_altura = altura - 150  
        
        self.config_tabuleiro['largura'] = nova_largura
        self.config_tabuleiro['altura'] = nova_altura
        self.config_tabuleiro['raio_buracos'] = min(nova_largura, nova_altura) * 0.1
        self.config_tabuleiro['espaco_centro_buracos'] = nova_largura * 0.13
        
        self.tabuleiro.config(width=nova_largura, height=nova_altura)
        self.tabuleiro.delete("all")
        self.desenhar_tabuleiro()
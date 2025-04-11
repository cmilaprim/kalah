import tkinter as tk
from tkinter import PhotoImage, messagebox

class StartScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#F0E6D2") 
        
        center_frame = tk.Frame(self, bg="#F0E6D2")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        titulo = tk.Label(center_frame, text="KALAH", font=("Helvetica", 52, "bold"), fg="#5C4033", bg="#F0E6D2")
        titulo.pack(pady=20)
        
        subtitulo = tk.Label(center_frame, text="De grão em grão... se vence a partida", font=("Helvetica", 24), fg="#5C4033", bg="#F0E6D2")
        subtitulo.pack(pady=10)
        
        estilo_botao = {
            'font': ('Helvetica', 18),
            'bg': '#8B4513',
            'fg': 'white',
            'activebackground': '#A0522D',
            'activeforeground': 'white',
            'relief': tk.RAISED,
            'borderwidth': 3,
            'padx': 20,
            'pady': 10,
            'width': 15
        }
        
        botao_iniciar = tk.Button(center_frame, text="Iniciar Partida", command=self.controller.start_game,**estilo_botao)
        botao_iniciar.pack(pady=20)
        
        botao_regras = tk.Button(center_frame, text="Regras do Jogo", command=self.mostrar_regras,**estilo_botao)
        botao_regras.pack(pady=10)
        
        botao_sair = tk.Button(center_frame, text="Sair", command=self.controller.root.quit, **estilo_botao)
        botao_sair.pack(pady=20)
        
    def mostrar_regras(self):
        """exibe as regras do jogo em uma caixa de diálogo"""
        regras = """
                    Regras do Kalah:
                    1. O jogo começa com 4 sementes em cada buraco.
                    2. No seu turno, escolha um buraco do seu lado para coletar todas as sementes.
                    3. Distribua as sementes no sentido anti-horário, uma em cada buraco.
                    4. Se a última semente cair em um buraco vazio do seu lado, capture essa semente e todas as sementes do buraco oposto.
                    5. Se a última semente cair no seu armazém, você ganha um turno extra.
                    6. O jogo termina quando todos os buracos de um lado estiverem vazios.
                    7. O jogador com mais sementes no final vence."""

        messagebox.showinfo("Regras do Kalah", regras)
    
    def redimensionar(self, largura, altura):
        """ajusta o tamanho e posição dos elementos quando a janela é redimensionada"""
        if hasattr(self, 'center_frame'):
            self.center_frame.place(relx=0.5, rely=0.5, anchor="center")
            
        if largura < 800:
            fonte_titulo = 36
            fonte_subtitulo = 18
            fonte_botoes = 14
        else:
            fonte_titulo = 52
            fonte_subtitulo = 24
            fonte_botoes = 18
        
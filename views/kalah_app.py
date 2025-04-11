import tkinter as tk
from tkinter import Menu
from .start_screen import StartScreen
from .game_screen import GameScreen

class KalahApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalah")
        self.root.geometry("1240x700")
        self.root.configure(bg="#F0E6D2")
                
        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)
        self.frames = {}
        
        self.setup_frames()
        self.show_frame("StartScreen")
        self.centraliza_tela()
        
        self.root.bind("<Configure>", self.on_window_resize)
    
    def on_window_resize(self, event):
        """centraliza a tela quando a janela é redimensionada"""
        if event.widget == self.root:
            largura = event.width
            altura = event.height
            
            for frame_name, frame in self.frames.items():
                if hasattr(frame, 'redimensionar'):
                    frame.redimensionar(largura, altura)
    
    def mostrar_regras(self):
        """exibe as regras do jogo"""
        if "StartScreen" in self.frames:
            self.frames["StartScreen"].mostrar_regras()
        
    def setup_frames(self):
        for F in (StartScreen, GameScreen):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
    
    def show_frame(self, frame_name):
        """traz a tela especificada para frente"""
        self.frames[frame_name].tkraise()
        
    def start_game(self):
        """inicia uma nova partida"""
        if "GameScreen" in self.frames:
            game_screen = self.frames["GameScreen"]
            game_screen.reiniciar_jogo() 
            self.show_frame("GameScreen")
        
    def centraliza_tela(self):
        """centraliza a janela na tela"""
        self.root.update_idletasks()
        largura_janela = self.root.winfo_width()
        altura_janela = self.root.winfo_height()
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        pos_x = (largura_tela - largura_janela) // 2
        pos_y = (altura_tela - altura_janela) // 2
        self.root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
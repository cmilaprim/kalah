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
        self.tabuleiro_width = 1300
        self.tabuleiro_height = 650
        self.raio_casas = self.tabuleiro_width * 0.06
        self.espaco_centro_casas = self.tabuleiro_width * 0.13
        
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

        player_name = simpledialog.askstring(title="Player Identification", prompt="Qual o seu nome?")
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name, self)
        messagebox.showinfo(message=message)
        
        
    def inicializar_janela(self) -> None:
        self.master.configure(bg='#F7F3E8')
        self.master.title("Tabuleiro de Kalah")
        self.master.geometry("1340x800")
        self.pack(fill=tk.BOTH, expand=True)
        self.create_menu()

    def criar_status_frame(self) -> None:
        self.status_frame = tk.Frame(self, bg=self.cores['fundo'], height=50)
        self.status_frame.pack(fill=tk.X, side=tk.TOP)
        self.status_label = tk.Label(self.status_frame,text="Vez do Jogador 1",font=("Helvetica", 16),bg=self.cores['fundo'],fg="#5C4033")
        self.status_label.pack(pady=10)
        
    def criar_canvas(self) -> None:
        self.canvas = tk.Canvas(self,width=self.tabuleiro_width,height=self.tabuleiro_height,bg=self.cores['tabuleiro'],highlightthickness=0)
        self.canvas.pack(padx=20, pady=20)
        self.canvas.bind("<Button-1>", self.click)

    def criar_botao_desistir(self) -> None:
        self.frame_botao = tk.Frame(self, bg=self.cores['fundo'])
        self.frame_botao.pack(fill=tk.X, pady=10)
        self.btn_desistir = tk.Button(self.frame_botao,text="DESISTIR",font=("Helvetica", 16, "bold"), bg=self.cores['botao_desistir'], fg=self.cores['texto_botoes'],command=self.desistir,width=15,padx=20,pady=5)
        self.btn_desistir.pack(pady=5)

    def create_menu(self) -> None:
        menu_bar = tk.Menu(self.master)
        menu_opcoes = tk.Menu(menu_bar, tearoff=0)
        menu_opcoes.add_command(label="Iniciar Partida", command=self.start_match)
        menu_opcoes.add_command(label="Reiniciar Jogo", command=self.recomecar_partida)
        menu_opcoes.add_command(label="Regras do Jogo", command=self.mostrar_regras)
        menu_opcoes.add_separator()
        menu_opcoes.add_command(label="Sair", command=self.master.quit)
        menu_bar.add_cascade(label="Menu", menu=menu_opcoes)
        self.master.config(menu=menu_bar)

    def comecar_partida(self) -> None:
        # self.game_started = True
        # self.controlador.comecar_partida()
        ...
    
    def start_match(self):
        start_status = self.dog_server_interface.start_match(2)
        message = start_status.get_message()
        messagebox.showinfo(message=message)
    
    def receive_start(self, start_status):
        message = start_status.get_message()
        messagebox.showinfo(message=message)
    
    def recomecar_partida(self) -> None:
        if not self.game_started:
            messagebox.showwarning("Atenção", "Você precisa iniciar a partida primeiro.")
            return
        print("strat_game")
        self.controlador.reiniciar_jogo()

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
        messagebox.showinfo("Regras do Jogo", regras)

    def desistir(self) -> None:
        confirma = messagebox.askyesno("Desistir","Tem certeza que deseja desistir da partida?")
        if not confirma:
            return
        messagebox.showinfo("Desistência", "Você desistiu da partida.")
        self.controlador.reiniciar_jogo()
    
    def click(self, event) -> None:
        if not self.game_started:
            return
        item = self.canvas.find_closest(event.x, event.y)
        for tag in self.canvas.gettags(item):
            if tag.startswith("casa_"):
                idx = int(tag.split("_",1)[1])
                if self.controlador.jogada_valida(idx):
                    self.controlador.realizar_jogada(idx)
                return

    def receber_jogada(self,posicao: int,jogador: int,estado_tabuleiro: List[List[int]],armazens: List[List[int]]) -> None:
        self.estado_tabuleiro = estado_tabuleiro
        self.armazens = armazens
        self.desenhar_tabuleiro()
        self.status_label.config(text=f"Vez do Jogador {jogador}")

    # def desenhar_tabuleiro(self) -> None:
    #     self.canvas.delete("all")
    #     prop = 0.5
    #     y_topo = self.tabuleiro_height * (1 - prop) / 2
    #     y_base = self.tabuleiro_height * (1 + prop) / 2

    #     self.canvas.create_text(self.tabuleiro_width/2, self.tabuleiro_height*0.02,text="Casas do Jogador 1", font=("Helvetica", 14),fill=self.cores['texto_botoes'])
    #     self.canvas.create_text(self.tabuleiro_width/2, self.tabuleiro_height*0.98,text="Casas do Jogador 2", font=("Helvetica", 14),fill=self.cores['texto_botoes'])

    #     x_start = (self.tabuleiro_width - 5*self.espaco_centro_casas)/2

    #     for idx, donos in enumerate(self.estado_tabuleiro):
    #         row = 0 if idx < 6 else 1
    #         col = idx if row == 0 else idx - 6
    #         x = x_start + col*self.espaco_centro_casas
    #         y = y_topo if row == 0 else y_base

    #         self.canvas.create_oval(x-self.raio_casas, y-self.raio_casas, x+self.raio_casas, y+self.raio_casas,fill=self.cores['casas'],outline=self.cores['borda_tabuleiro'],width=4,tags=(f"casa_{idx}",))

    #         seed_r = 10
    #         for i, dono in enumerate(donos):
    #             ang = math.radians(i * (360/max(1,len(donos))))
    #             rx = x + self.raio_casas*0.45*math.cos(ang)
    #             ry = y + self.raio_casas*0.45*math.sin(ang)
    #             cor = (self.cores['sementes'])
    #             self.canvas.create_oval(rx-seed_r, ry-seed_r, rx+seed_r, ry+seed_r,fill=cor, outline="")
    #         self.canvas.create_text(x, y, text=str(len(donos)), font=("Helvetica", 14, "bold"),fill=self.cores['texto_botoes'])

    #     # armazém J1 (à esquerda)
    #     self.canvas.create_rectangle(20, y_topo, 100, y_base,fill=self.cores['casas'],outline=self.cores['borda_tabuleiro'], width=3)
    #     self.canvas.create_text(60, (y_topo + y_base)/2,text=str(len(self.armazens[0])),font=("Helvetica", 16, "bold"),fill=self.cores['texto_botoes'])
    #     self.canvas.create_text(60, y_base + 20,text="Armazém J1",font=("Helvetica", 12),fill=self.cores['texto_botoes'])

    #     # armazém J2 (à direita)
    #     warehouse_width = 80
    #     warehouse_margin = 20
    #     x2 = self.tabuleiro_width - warehouse_margin
    #     x1 = x2 - warehouse_width

    #     self.canvas.create_rectangle(x1, y_topo, x2, y_base,fill=self.cores['casas'],outline=self.cores['borda_tabuleiro'],width=3)
    #     cx = (x1 + x2)/2
    #     self.canvas.create_text(cx, (y_topo + y_base)/2,text=str(len(self.armazens[1])),font=("Helvetica", 16, "bold"),fill=self.cores['texto_botoes'])
    #     self.canvas.create_text(cx, y_base + 20,text="Armazém J2",font=("Helvetica", 12),fill=self.cores['texto_botoes'])

    def desenhar_tabuleiro(self) -> None:
        self.canvas.delete("all")
        prop = 0.5
        y_topo = self.tabuleiro_height * (1 - prop) / 2
        y_base = self.tabuleiro_height * (1 + prop) / 2

        self.canvas.create_text(self.tabuleiro_width/2, self.tabuleiro_height*0.02,text="Casas do Jogador 1", font=("Helvetica", 14),fill=self.cores['texto_botoes'])
        self.canvas.create_text(self.tabuleiro_width/2, self.tabuleiro_height*0.98,text="Casas do Jogador 2", font=("Helvetica", 14),fill=self.cores['texto_botoes'])

        x_start = (self.tabuleiro_width - 5*self.espaco_centro_casas)/2

        for idx, quantidade_lista in enumerate(self.estado_tabuleiro):
            row = 0 if idx < 6 else 1
            col = idx if row == 0 else idx - 6
            x = x_start + col*self.espaco_centro_casas
            y = y_topo if row == 0 else y_base

            # Cria a casa
            self.canvas.create_oval(x-self.raio_casas, y-self.raio_casas, x+self.raio_casas, y+self.raio_casas,fill=self.cores['casas'],outline=self.cores['borda_tabuleiro'],width=4,tags=(f"casa_{idx}",))

            quantidade = quantidade_lista[0] 
            
            if quantidade > 0:
                seed_r = 10
                sementes_para_mostrar = min(quantidade, 12)
                
                for i in range(sementes_para_mostrar):
                    ang = math.radians(i * (360/sementes_para_mostrar))
                    rx = x + self.raio_casas*0.45*math.cos(ang)
                    ry = y + self.raio_casas*0.45*math.sin(ang)
                    self.canvas.create_oval(rx-seed_r, ry-seed_r, rx+seed_r, ry+seed_r,fill=self.cores['sementes'], outline="")
                    
            self.canvas.create_text(x, y, text=str(quantidade), font=("Helvetica", 14, "bold"),fill=self.cores['texto_botoes'])

        self.canvas.create_rectangle(20, y_topo, 100, y_base,fill=self.cores['casas'],outline=self.cores['borda_tabuleiro'], width=3)
        self.canvas.create_text(60, (y_topo + y_base)/2, text=str(self.armazens[0][0]), font=("Helvetica", 16, "bold"),fill=self.cores['texto_botoes'])
        self.canvas.create_text(60, y_base + 20,text="Armazém J1",font=("Helvetica", 12),fill=self.cores['texto_botoes'])

        # armazém J2 (à direita)
        warehouse_width = 80
        warehouse_margin = 20
        x2 = self.tabuleiro_width - warehouse_margin
        x1 = x2 - warehouse_width

        self.canvas.create_rectangle(x1, y_topo, x2, y_base,fill=self.cores['casas'],outline=self.cores['borda_tabuleiro'],width=3)
        cx = (x1 + x2)/2
        self.canvas.create_text(cx, (y_topo + y_base)/2,text=str(self.armazens[1][0]),font=("Helvetica", 16, "bold"),fill=self.cores['texto_botoes'])
        self.canvas.create_text(cx, y_base + 20,text="Armazém J2",font=("Helvetica", 12),fill=self.cores['texto_botoes'])

    def informar_vencedor(self, vencedor: int) -> None:
        messagebox.showinfo("Fim de Jogo", f"O vencedor é o Jogador {vencedor}!")
        
    def informar_empate(self) -> None:
        messagebox.showinfo("Fim de Jogo", "Empate! Ambos têm o mesmo número de sementes.")
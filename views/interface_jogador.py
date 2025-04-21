import tkinter as tk
from tkinter import ttk, messagebox
import math
from typing import List, Any


class InterfaceJogador(ttk.Frame):
    def __init__(self, master: tk.Tk, controlador: Any) -> None:
        style = ttk.Style()
        style.configure('My.TFrame', background='#F7F3E8')
        
        super().__init__(master, style='My.TFrame')
        self.master = master
        self.master.configure(bg='#F7F3E8')

        self.controlador = controlador
        self.master.title("Tabuleiro de Kalah")
        self.master.geometry("1340x800")
        self.pack(fill=tk.BOTH, expand=True)

        self._create_menu()

        #dimensões do canvas
        self.tabuleiro_width = 1300
        self.tabuleiro_height = 650

        #raio e espaçamento das casas (proporcional à largura)
        self.percentual_raio_casa = 0.06
        self.percentual_espaco_centro = 0.13
        self.raio_casas = self.tabuleiro_width * self.percentual_raio_casa
        self.espaco_centro_casas = self.tabuleiro_width * self.percentual_espaco_centro

        self.cores = {
            'fundo': "#F7F3E8",
            'tabuleiro': "#8B4513",
            'borda_tabuleiro': "#5D3A1A",
            'casas': "#E6D2B5",
            # 'sementes_jogador1': '#7D8C5B',
            'sementes': '#A47551',
            'texto_botoes': '#FFFFFF',
            'botao_desistir': '#FF0000',
        }
        
        # status no topo
        self.status_frame = tk.Frame(self, bg=self.cores['fundo'], height=50)
        self.status_frame.pack(fill=tk.X, side=tk.TOP)
        self.status_label = tk.Label(self.status_frame,text="Vez do Jogador 1",font=("Helvetica", 16),bg=self.cores['fundo'],fg="#5C4033")
        self.status_label.pack(pady=10)
        
        #canvas do tabuleiro
        self.canvas = tk.Canvas(self,width=self.tabuleiro_width,height=self.tabuleiro_height,bg=self.cores['tabuleiro'],highlightthickness=0)
        self.canvas.pack(padx=20, pady=20)

        self.canvas.bind("<Button-1>", self._on_click)

        #botão desistir embaixo
        self.frame_botao = tk.Frame(self, bg=self.cores['fundo'])
        self.frame_botao.pack(fill=tk.X, pady=10)
        self.btn_desistir = tk.Button(self.frame_botao,text="DESISTIR",font=("Helvetica", 16, "bold"),bg=self.cores['botao_desistir'],fg=self.cores['texto_botoes'],command=self.controlador.jogo_terminou,width=15,padx=20,pady=5)
        self.btn_desistir.pack(pady=5)

        #estado do jogo
        self.coords_casas = []

    def _create_menu(self) -> None:
        menu_bar = tk.Menu(self.master)
        menu_opcoes = tk.Menu(menu_bar, tearoff=0)
        menu_opcoes.add_command(label="Iniciar Partida", command=self._iniciar_partida)
        menu_opcoes.add_command(label="Regras do Jogo", command=self._mostrar_regras)
        menu_opcoes.add_separator()
        menu_opcoes.add_command(label="Sair", command=self.master.quit)
        menu_bar.add_cascade(label="Menu", menu=menu_opcoes)
        self.master.config(menu=menu_bar)

    def _iniciar_partida(self) -> None:
        self.controlador.reiniciar_jogo()

    def _mostrar_regras(self) -> None:
        regras = (
            "Regras do Kalah:\n"
            "1. O jogo começa com 4 sementes em cada buraco.\n"
            "2. No seu turno, escolha um buraco do seu lado para coletar todas as sementes.\n"
            "3. Distribua as sementes no sentido anti-horário, uma em cada buraco, pulando o armazém do oponente.\n"
            "4. Se a última semente cair em um buraco vazio do seu lado e o buraco oposto tiver sementes, você captura todas.\n"
            "5. Se a última cair no seu armazém, você joga novamente.\n"
            "6. O jogo termina quando todas as casas de um lado estiverem vazias.\n"
            "7. Quem tiver mais sementes no armazém vence."
        )
        messagebox.showinfo("Regras do Jogo", regras)

    def _on_click(self, event):
        for i, (x, y) in enumerate(self.coords_casas):
            if (event.x - x)**2 + (event.y - y)**2 <= self.raio_casas**2:
                self.controlador.realizar_jogada(i)
                break

    def update_status(self, jogador: int) -> None:
        self.status_label.config(text=f"Vez do Jogador {jogador}")

    def receive_move(self, posicao: int, jogador: int,estado_tabuleiro: List[int], armazens: List[int]) -> None:
        self.estado_tabuleiro = estado_tabuleiro
        self.armazens = armazens
        self._desenhar_tabuleiro()
        self.update_status(jogador)

    def inform_winner(self, vencedor: int) -> None:
        messagebox.showinfo("Fim de Jogo", f"O vencedor é o Jogador {vencedor}!")

    def _desenhar_tabuleiro(self):
        #limpa tudo
        self.canvas.delete("all")

        #calcula as linhas verticais do tabuleiro: de 25% a 75% da altura
        region_prop = 0.5
        y_topo  = self.tabuleiro_height * (1 - region_prop) / 2  # = 0.25 * height
        y_base  = self.tabuleiro_height * (1 + region_prop) / 2  # = 0.75 * height

        self.canvas.create_text(self.tabuleiro_width/2, self.tabuleiro_height*0.02,text="Casas do Jogador 1", font=("Helvetica", 14),fill=self.cores['texto_botoes'])
        self.canvas.create_text(self.tabuleiro_width/2, self.tabuleiro_height*0.98,text="Casas do Jogador 2", font=("Helvetica", 14),fill=self.cores['texto_botoes'])

        #desenha casas
        x_inicio = (self.tabuleiro_width - 5 * self.espaco_centro_casas) / 2
        self.coords_casas.clear()
        for i in range(6):
            x = x_inicio + i * self.espaco_centro_casas
            self._desenhar_casa(x, y_topo, self.estado_tabuleiro[i], self.cores['sementes'])
            self.coords_casas.append((x, y_topo))
        for i in range(6, 12):
            x = x_inicio + (i-6) * self.espaco_centro_casas
            self._desenhar_casa(x, y_base, self.estado_tabuleiro[i], self.cores['sementes'])
            self.coords_casas.append((x, y_base))

        #armazém J1 fixo à esquerda
        self.canvas.create_rectangle(20, y_topo, 100, y_base,fill=self.cores['casas'],outline=self.cores['borda_tabuleiro'], width=3)
        self.canvas.create_text(60, (y_topo + y_base)/2,text=str(len(self.armazens[0])), font=("Helvetica", 16, "bold"),fill=self.cores['texto_botoes'])
        self.canvas.create_text(60, y_base + 20,text="Armazém J1", font=("Helvetica", 12),fill=self.cores['texto_botoes'])

        #armazém J2 alinhado dinamicamente à direita
        warehouse_width  = 80
        warehouse_margin = 20
        x2 = self.tabuleiro_width - warehouse_margin
        x1 = x2 - warehouse_width

        self.canvas.create_rectangle(x1, y_topo, x2, y_base,fill=self.cores['casas'],outline=self.cores['borda_tabuleiro'], width=3)
        cx = (x1 + x2)/2
        self.canvas.create_text(cx, (y_topo + y_base)/2,text=str(len(self.armazens[1])), font=("Helvetica", 16, "bold"),fill=self.cores['texto_botoes'])
        self.canvas.create_text(cx, y_base + 20,text="Armazém J2", font=("Helvetica", 12),fill=self.cores['texto_botoes'])

    def _desenhar_casa(self, x: float, y: float, donos: List[int], _dummy):
        #primeiro, o buraco
        self.canvas.create_oval(
            x-self.raio_casas, y-self.raio_casas,
            x+self.raio_casas, y+self.raio_casas,
            fill=self.cores['casas'],
            outline=self.cores['borda_tabuleiro'], width=4
        )
        #depois, uma bolinha por semente, cor conforme dono
        raio = 10
        for i, dono in enumerate(donos):
            angle = math.radians(i * (360 / max(1, len(donos))))
            rx = x + self.raio_casas*0.45*math.cos(angle)
            ry = y + self.raio_casas*0.45*math.sin(angle)
            cor = (self.cores['sementes']
                if dono == 1 else
                self.cores['sementes'])
            self.canvas.create_oval(rx-raio, ry-raio, rx+raio, ry+raio,fill=cor)

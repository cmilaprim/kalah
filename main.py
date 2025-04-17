import tkinter as tk
from controllers.jogo_tabuleiro import JogoTabuleiro

def main():
    root = tk.Tk()
    root.title("Jogo Kalah")
    root.geometry("1240x650")
    root.configure(bg="#F0E6D2")
    JogoTabuleiro(root)
    root.mainloop()


if __name__ == "__main__":
    main()
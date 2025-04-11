import tkinter as tk
import sys
import os
from views.kalah_app import KalahApp

def main():
    root = tk.Tk()
    app = KalahApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
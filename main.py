import tkinter as tk
from Jogador import Jogador
from Quiz import Quiz

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('500x500')
    quiz_app = Quiz(root)
    root.mainloop()
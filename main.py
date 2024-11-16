import tkinter as tk
from Quiz import Quiz

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('750x500')
    quiz_app = Quiz(root)
    root.mainloop()
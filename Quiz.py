import sqlite3
import tkinter as tk
from Jogador import Jogador

class Quiz():

    perguntas_total = None
    perguntas_selecionadas = None


    def __init__(self, root):
        self.root = root
        self.root.title('Quiz!')
        self.tela_inicial()

    def tela_inicial(self):
        title_label = tk.Label(self.root, text="Bem-Vindos ao Quiz!", font=("Arial", 24))
        title_label.pack(pady=20)





    def criar_banco_dados(self):
        conn = sqlite3.connect('quiz.db')
        c = conn.cursor()

        # Tabela de perguntas
        c.execute('''CREATE TABLE IF NOT EXISTS perguntas (
                        id INTEGER PRIMARY KEY,
                        question TEXT,
                        option1 TEXT,
                        option2 TEXT,
                        option3 TEXT,
                        option4 TEXT,
                        correct INTEGER)''')

        # Tabela de jogadores
        c.execute('''CREATE TABLE IF NOT EXISTS jogadores (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE,
                        password TEXT)''')

        # Tabela de resultados
        c.execute('''CREATE TABLE IF NOT EXISTS resultados (
                        id INTEGER PRIMARY KEY,
                        jogador_id INTEGER,
                        tempo REAL,
                        acertos INTEGER,
                        nome TEXT,
                        FOREIGN KEY(jogador_id) REFERENCES jogadores(id))''')

        conn.commit()
        conn.close()

        # Carregar perguntas do CSV
        #TODO: carregar perguntas para tabela da BD




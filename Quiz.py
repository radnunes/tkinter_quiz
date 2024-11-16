import csv
import sqlite3
import tkinter as tk
from Jogador import Jogador

class Quiz():

    def __init__(self, root):
        self.root = root
        self.root.title('Quiz!')
        self.current_frame = None
        self.jogador = None
        self.questions = []
        self.current_question = 0
        self.correct_answers = 0
        self.start_time = None
        self.selected_difficulty = None
        self.criar_bd()
        self.show_login_frame()

    def tela_inicial(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        self.root.grid_columnconfigure(4, weight=1)
        self.root.grid_columnconfigure(5, weight=1)

        title_label = tk.Label(self.root, text="Bem-Vindos ao Quiz!", font=("Arial", 24))
        title_label.grid(row=0, column=1, columnspan=4, pady=20)

        username_label = tk.Label(self.root, text="Nome:", font=("Arial",12))
        username_label.grid(row=1, column=2, pady=10)

        password_label = tk.Label(self.root, text="Senha:", font=("Arial", 12))
        password_label.grid(row=2, column=2, pady=10)

        username_entry = tk.Entry(self.root)
        username_entry.grid(row=1, column=3, pady=10)

        password_entry = tk.Entry(self.root)
        password_entry.grid(row=2, column=3, pady=10)

        login_button = tk.Button(self.root, text="Login", font=("Arial", 16))
        login_button.grid(row=3, column=2, padx=10, pady=10)

        guest_button = tk.Button(self.root, text="Registar", font=("Arial", 16))
        guest_button.grid(row=3, column=3, padx=10, pady=10)

        login_button = tk.Button(self.root, text="Convidado", font=("Arial", 16))
        login_button.grid(row=4, column=2, padx=10, pady=10)

        guest_button = tk.Button(self.root, text="Ranking", font=("Arial", 16))
        guest_button.grid(row=4, column=3, padx=10, pady=10)



    def criar_bd(self):
        conn = sqlite3.connect('quiz.db')
        c = conn.cursor()

        c.execute('DROP TABLE IF EXISTS perguntas')
        c.execute('DROP TABLE IF EXISTS jogadores')
        c.execute('DROP TABLE IF EXISTS resultados')

        # Tabela de perguntas
        c.execute('''CREATE TABLE IF NOT EXISTS perguntas (
                        id INTEGER PRIMARY KEY,
                        pergunta TEXT,
                        opcao1 TEXT,
                        opcao2 TEXT,
                        opcao3 TEXT,
                        opcao4 TEXT,
                        correta INTEGER)''')

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
        print('BD criada com sucesso')

        # Carregar perguntas do CSV
        Quiz.carregar_perguntas(self)

    def carregar_perguntas(self):
        conn = sqlite3.connect('quiz.db')
        cursor = conn.cursor()

        try:
            with open('questions.csv', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    cursor.execute('''
                        INSERT INTO perguntas (pergunta, opcao1, opcao2, opcao3, opcao4, correta)
                        VALUES (?, ?, ?, ?, ?, ?)
                        ''', (
                        row['question'],
                        row['option1'],
                        row['option2'],
                        row['option3'],
                        row['option4'],
                        int(row['correct'])
                    ))
            conn.commit()
            print('Perguntas carregadas com sucesso')
        except Exception as e:
            print(f"Erro: {e}")
        finally:
            conn.close()

    def guest(self):
        return Jogador(self.root, self.perguntas_selecionadas)
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

    def clear_frame(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack(fill='both', expand=True)

    def show_login_frame(self):
        self.clear_frame()

        title_label = tk.Label(self.current_frame, text="Bem-Vindos ao Quiz!", font=("Arial", 24))
        title_label.pack(pady=20)

        # Login fields
        tk.Label(self.current_frame, text="Nome:", font=("Arial", 12)).pack(pady=5)
        self.username_entry = tk.Entry(self.current_frame)
        self.username_entry.pack(pady=5)

        tk.Label(self.current_frame, text="Senha:", font=("Arial", 12)).pack(pady=5)
        self.password_entry = tk.Entry(self.current_frame, show="*")
        self.password_entry.pack(pady=5)

        # Buttons
        tk.Button(self.current_frame, text="Login", font=("Arial", 16),
                  command=self.handle_login).pack(pady=10)
        tk.Button(self.current_frame, text="Registar", font=("Arial", 16),
                  command=self.show_register_frame).pack(pady=10)
        tk.Button(self.current_frame, text="Convidado", font=("Arial", 16),
                  command=self.play_as_guest).pack(pady=10)
        tk.Button(self.current_frame, text="Ranking", font=("Arial", 16),
                  command=self.show_leaderboard).pack(pady=10)

    def show_register_frame(self):
        self.clear_frame()

        title_label = tk.Label(self.current_frame, text="Registar Nova Conta", font=("Arial", 24))
        title_label.pack(pady=20)

        tk.Label(self.current_frame, text="Nome:", font=("Arial", 12)).pack(pady=5)
        self.reg_username = tk.Entry(self.current_frame)
        self.reg_username.pack(pady=5)

        tk.Label(self.current_frame, text="Senha:", font=("Arial", 12)).pack(pady=5)
        self.reg_password = tk.Entry(self.current_frame, show="*")
        self.reg_password.pack(pady=5)

        tk.Label(self.current_frame, text="Confirmar Senha:", font=("Arial", 12)).pack(pady=5)
        self.reg_confirm = tk.Entry(self.current_frame, show="*")
        self.reg_confirm.pack(pady=5)

        tk.Button(self.current_frame, text="Registar", font=("Arial", 16),
                  command=self.handle_register).pack(pady=10)
        tk.Button(self.current_frame, text="Voltar", font=("Arial", 16),
                  command=self.show_login_frame).pack(pady=10)



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
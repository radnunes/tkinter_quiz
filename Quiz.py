import csv
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
        self.criar_bd()

    def tela_inicial(self):
        title_label = tk.Label(self.root, text="Bem-Vindos ao Quiz!", font=("Arial", 24))
        title_label.pack(pady=20)





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


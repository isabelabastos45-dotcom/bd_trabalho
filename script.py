import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3

conn = sqlite3.connect('gestao_clientes.db')
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

#detelar e recriar por conta do ON DETELE CASCADE
cursor.execute("""
DROP TABLE IF EXISTS cliente_telefones;
""")
cursor.execute("""
DROP TABLE IF EXISTS clientes;
""")
conn.commit()

#criar tabelas
cursor.execute("""
CREATE TABLE clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(150) NOT NULL,
    idade INTEGER,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    endereco TEXT,
    localidade VARCHAR(100),
    data_nascimento DATE,
    status INTEGER NOT NULL CHECK (status IN (0,1))
);
""")

cursor.execute("""
CREATE TABLE cliente_telefones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero VARCHAR(20),
    tipo VARCHAR(100),
    cliente_id INTEGER,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);
""")

print("Tabelas criadas com sucesso")

#adicionar informações em clientes
clientes = [
    ('Isabela Bento Bastos', 16, '12345678915', 'isabela.bento@gmail.com', 'Rua Vermelha', 'Fortaleza', '2009-02-01', 1),
    ('Júlia Lins de Alencar', 17, '12345678815', 'julia.lins@gmail.com', 'Rua Laranja', 'Fortaleza', '2009-02-02', 1),
    ('Letícia Ozório de Lemos', 17, '12345678715', 'leticia.ozorio@gmail.com', 'Rua Amarela', 'Fortaleza', '2009-02-03', 1),
    ('Loren Maria Félix Lessa', 17, '12345678615', 'loren.felix@gmail.com', 'Rua Verde', 'Fortaleza', '2009-02-04', 1),
    ('Mauricio Ferreira', 17, '12345679915', 'mauricio.ferreira@gmail.com', 'Rua Azul', 'Fortaleza', '2009-02-05', 1)
]

cursor.executemany("""
INSERT INTO clientes (nome, idade, cpf, email, endereco, localidade, data_nascimento, status)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", clientes)


#adicionar informações em cliente_telefones
cliente_telefones = [
    ('111', 'Fixo', 1),
    ('222', 'WhatsApp', 2),
    ('333', 'Telefone', 3),
    ('444', 'Fixo', 4),
    ('555', 'Telefone', 5)
]

cursor.executemany("""
INSERT INTO cliente_telefones (numero, tipo, cliente_id)
VALUES (?, ?, ?)
""", cliente_telefones)

conn.commit()

print("Dados inseridos com sucesso")

#interface
janela = Tk()
janela.title('Gestão de Clientes')

tree = ttk.Treeview(janela, selectmode = "browse", column = ("coluna1", "coluna2", "coluna3", "coluna4", "coluna5"), show = 'headings')

tree.column("coluna1", width = 50, minwidth = 50, stretch = NO, anchor = CENTER)
tree.heading("#1", text = 'ID')
tree.column("coluna2", width = 200, minwidth = 50, stretch = NO, anchor = CENTER)
tree.heading("#2", text = 'Nome')
tree.column("coluna3", width = 200, minwidth = 50, stretch = NO, anchor = CENTER)
tree.heading("#3", text = 'CPF')
tree.column("coluna4", width = 200, minwidth = 50, stretch = NO, anchor = CENTER)
tree.heading("#4", text = 'Email')
tree.column("coluna5", width = 100, minwidth = 50, stretch = NO, anchor = CENTER)
tree.heading("#5", text = 'Ações')

tree.grid(row = 0, column = 0)

cursor.execute("""
SELECT id, nome, cpf, email FROM CLIENTES;
""")

for row in cursor.fetchall():
    tree.insert("", END, values = row)

conn.close()
janela.mainloop()
import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3
#teste do vs code no mac
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
    ('Isabela Bento Bastos', 16, '12345678910', 'isabela.bento@gmail.com', 'Rua Verde, 01', 'Fortaleza', '2009-02-01', 1),
    ('Júlia Lins de Alencar', 17, '12345678811', 'julia.lins@gmail.com', 'Rua Roxo, 02', 'Fortaleza', '2008-02-02', 0),
    ('Letícia Ozório de Lemos', 17, '12345678712', 'leticia.ozorio@gmail.com', 'Rua Rosa, 03', 'Fortaleza', '2008-02-03', 1),
    ('Loren Maria Félix Lessa', 17, '12345678613', 'loren.felix@gmail.com', 'Rua Azul, 04', 'Fortaleza', '2008-02-04', 0),
    ('Maurício Ferreira Lima Junior', 17, '12345679914', 'mauricio.ferreira@gmail.com', 'Rua Vermelha, 05', 'Fortaleza', '2008-02-05', 1)

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

def adicionar_cliente():
    def salvar():
        conn = sqlite3.connect('gestao_clientes.db')
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO clientes (nome, idade, cpf, email, endereco, localidade, data_nascimento, status)
        VALUES (?, ?, ?, ?, '', '', '', 1)
        """, (
            entry_nome.get(),
            entry_idade.get(),
            entry_cpf.get(),
            entry_email.get()
        ))
        conn.commit()
        novo_id = cursor.lastrowid
        tree.insert("", END, values=(novo_id, entry_nome.get(), entry_cpf.get(), entry_email.get()))
        tela.destroy()

    tela = Toplevel(janela)
    tela.title("Adicionar Cliente")

    Label(tela, text="Nome").grid(row=0, column=0)
    entry_nome = Entry(tela)
    entry_nome.grid(row=0, column=1)

    Label(tela, text="Idade").grid(row=1, column=0)
    entry_idade = Entry(tela)
    entry_idade.grid(row=1, column=1)

    Label(tela, text="CPF").grid(row=2, column=0)
    entry_cpf = Entry(tela)
    entry_cpf.grid(row=2, column=1)

    Label(tela, text="Email").grid(row=3, column=0)
    entry_email = Entry(tela)
    entry_email.grid(row=3, column=1)

    Button(tela, text="Salvar", command=salvar).grid(row=4, column=0, columnspan=2)


def editar_cliente():
    selecionado = tree.focus()
    if not selecionado:
        return

    valores = tree.item(selecionado, 'values')
    cliente_id = valores[0]

    def salvar_edicao():
        conn = sqlite3.connect('gestao_clientes.db')
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE clientes SET nome=?, cpf=?, email=? WHERE id=?
        """, (
            entry_nome.get(),
            entry_cpf.get(),
            entry_email.get(),
            cliente_id
        ))
        conn.commit()
        tree.item(selecionado, values=(cliente_id, entry_nome.get(), entry_cpf.get(), entry_email.get(), "Editar"))
        tela.destroy()

    tela = Toplevel(janela)
    tela.title("Editar Cliente")

    Label(tela, text="Nome").grid(row=0, column=0)
    entry_nome = Entry(tela)
    entry_nome.insert(0, valores[1])
    entry_nome.grid(row=0, column=1)

    Label(tela, text="CPF").grid(row=1, column=0)
    entry_cpf = Entry(tela)
    entry_cpf.insert(0, valores[2])
    entry_cpf.grid(row=1, column=1)

    Label(tela, text="Email").grid(row=2, column=0)
    entry_email = Entry(tela)
    entry_email.insert(0, valores[3])
    entry_email.grid(row=2, column=1)

    Button(tela, text="Salvar Alterações", command=salvar_edicao).grid(row=3, column=0, columnspan=2)


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

frame_botoes = Frame(janela)
frame_botoes.grid(row=1, column=0, pady=10)

Button(frame_botoes, text="Adicionar Cliente", command=adicionar_cliente).grid(row=0, column=0, padx=5)
Button(frame_botoes, text="Editar Cliente", command=editar_cliente).grid(row=0, column=1, padx=5)


cursor.execute("""
SELECT id, nome, cpf, email FROM CLIENTES;
""")

tree.insert("", END, values=(novo_id, entry_nome.get(), entry_cpf.get(), entry_email.get(), "Editar"))

def clique_duplo(event):
    item = tree.identify_row(event.y)
    coluna = tree.identify_column(event.x)

    if coluna == '#5' and item:
        tree.selection_set(item)
        tree.focus(item)
        editar_cliente()

conn.close()
janela.mainloop()

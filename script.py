import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect('gestao_clientes.db')
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

#detelar e recriar por conta do ON DETELE CASCADE 
cursor.execute("DROP TABLE IF EXISTS cliente_telefones;")
cursor.execute("DROP TABLE IF EXISTS clientes;")
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
    numeros VARCHAR(20),
    tipo VARCHAR(100),
    cliente_id INTEGER,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);
""")

#adicionar informações em clientes
clientes = [
    ('Isaac Bento Bastos', 16, '12345678915', 'isaac.bento@gmail.com', 'Rua Vermelha, 01', 'Fortaleza', '2009-02-01', 1),
    ('Júlia Lins de Alencar', 17, '12345678815', 'julia.lins@gmail.com', 'Rua Laranja, 02', 'Fortaleza', '2009-02-02', 1),
    ('Letícia Ozório de Lemos', 17, '12345678715', 'leticia.ozorio@gmail.com', 'Rua Amarela, 03', 'Fortaleza', '2009-02-03', 1),
    ('Loren Maria Félix Lessa', 17, '12345678615', 'loren.felix@gmail.com', 'Rua Verde, 04', 'Fortaleza', '2009-02-04', 1),
    ('Mauricio Ferreira', 17, '12345679915', 'mauricio.ferreira@gmail.com', 'Rua Azul, 05', 'Fortaleza', '2009-02-05', 1)
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
INSERT INTO cliente_telefones (numeros, tipo, cliente_id)
VALUES (?, ?, ?)
""", cliente_telefones)

conn.commit()

#interface
janela = Tk()
janela.title('Gestão de Clientes')
janela.geometry("800x400")

frame_tabela = Frame(janela)
frame_tabela.pack(fill=BOTH, expand=True, padx=10, pady=10)

tree = ttk.Treeview(frame_tabela, columns=("id","nome","cpf","email","acao"), show="headings")
tree.pack(fill=BOTH, expand=True)

for col, txt, w in [
    ("id","ID",50),
    ("nome","Nome",250),
    ("cpf","CPF",120),
    ("email","Email",250),
    ("acao","Ações",100)
]:
    tree.heading(col, text=txt)

    if col == "acao":
        tree.column(col, width=w, anchor=CENTER)
    else:
        tree.column(col, width=w, anchor=CENTER)

#atualizar a tabela
def atualizar_tree():
    for item in tree.get_children():
        tree.delete(item)
    cursor.execute("SELECT id, nome, cpf, email FROM clientes;")
    for row in cursor.fetchall():
        tree.insert("", END, values=(row[0], row[1], row[2], row[3], "Editar | Deletar"))

atualizar_tree()

#botão
frame_botoes = Frame(janela)
frame_botoes.pack(pady=10)

#listar detalhes
def visualizar_cliente(event):
    item = tree.identify_row(event.y)
    coluna = tree.identify_column(event.x)

    if not item or coluna != '#2':
        return

    id_cliente = tree.item(item, 'values')[0]

    conn = sqlite3.connect('gestao_clientes.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nome, idade, cpf, email, endereco, localidade, data_nascimento, status
        FROM clientes
        WHERE id = ?
    """, (id_cliente,))
    cliente = cursor.fetchone()

    cursor.execute("""
        SELECT numeros, tipo
        FROM cliente_telefones
        WHERE cliente_id = ?
    """, (id_cliente,))
    telefones = cursor.fetchall()
    conn.close()
    
    if not cliente:
        return

    tela = Toplevel(janela)
    tela.title("Detalhes do Cliente")
    tela.resizable(False, False)

    labels = ["Nome","Idade","CPF","Email","Endereço","Localidade","Data de Nascimento","Status","Telefones"]

    telefones_texto = "\n".join([f"{num} ({tipo})" for num, tipo in telefones]) if telefones else "Nenhum"

    valores = list(cliente) + [telefones_texto]

    for i, (label, valor) in enumerate(zip(labels, valores)):
        Label(tela, text=label+":", font=("Arial", 10, "bold")).grid(row=i, column=0, sticky="w", padx=10, pady=5)
        Label(tela, text=valor).grid(row=i, column=1, sticky="w", padx=10, pady=5)

tree.bind("<Double-1>", visualizar_cliente)

#adicionar clientes
def adicionar_cliente():
    tela = Toplevel(janela)
    tela.title("Adicionar Cliente")
    tela.geometry("260x400")

    labels = ["Nome","Idade","CPF","Email","Endereço","Localidade","Data de nascimento","Status"]
    entradas = []

    for i, l in enumerate(labels):
        Label(tela, text=l).grid(row=i, column=0, sticky="w", padx=5, pady=5)
        e = Entry(tela)
        e.grid(row=i, column=1, padx=5, pady=5)
        entradas.append(e)

    Label(tela, text="Telefones").grid(row=8, column=0, columnspan=2)

    telefones_frame = Frame(tela)
    telefones_frame.grid(row=9, column=0, columnspan=2)

    telefone_entries = []

    def adicionar_telefone():
        frame = Frame(telefones_frame)
        frame.pack(pady=2)

        n = Entry(frame, width=15)
        n.pack(side=LEFT, padx=2)

        t = Entry(frame, width=15)
        t.pack(side=LEFT, padx=2)

        telefone_entries.append((n,t))

    Button(tela, text="Adicionar Telefone", command=adicionar_telefone)\
        .grid(row=10, column=0, columnspan=2, pady=5)

    adicionar_telefone()

    def salvar():
        cursor.execute("""
        INSERT INTO clientes VALUES (NULL,?,?,?,?,?,?,?,?)
        """, [e.get() for e in entradas])

        cliente_id = cursor.lastrowid

        for n,t in telefone_entries:
            if n.get():
                cursor.execute("""
                INSERT INTO cliente_telefones VALUES (NULL,?,?,?)
                """, (n.get(), t.get(), cliente_id))

        conn.commit()
        atualizar_tree()
        tela.destroy()

    Button(tela, text="Salvar Cliente", command=salvar)\
        .grid(row=11, column=0, columnspan=2, pady=10)
    
Button(
    frame_botoes,
    text="Adicionar Cliente",
    width=20,
    command=adicionar_cliente
    ).pack()


#editar informações
def editar_cliente(cliente_id):
    conn = sqlite3.connect('gestao_clientes.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nome, idade, cpf, email, endereco, localidade, data_nascimento, status
        FROM clientes WHERE id=?
    """, (cliente_id,))
    cliente = cursor.fetchone()

    cursor.execute("""
        SELECT id, numeros, tipo
        FROM cliente_telefones
        WHERE cliente_id=?
    """, (cliente_id,))
    telefones = cursor.fetchall()
    
    tela = Toplevel(janela)
    tela.title("Editar Cliente")
    tela.geometry("300x400")

    labels = ["Nome","Idade","CPF","Email","Endereço","Localidade","Data Nascimento","Status"]
    entries = []

    for i, l in enumerate(labels):
        Label(tela, text=l).grid(row=i, column=0, sticky="w", padx=5, pady=3)
        e = Entry(tela)
        e.grid(row=i, column=1, padx=5, pady=3)
        e.insert(0, cliente[i])
        entries.append(e)

    entry_nome, entry_idade, entry_cpf, entry_email, entry_endereco, entry_localidade, entry_data, entry_status = entries

    Label(tela, text="Telefones").grid(row=8, column=0, columnspan=2, pady=5)
    telefones_frame = Frame(tela)
    telefones_frame.grid(row=9, column=0, columnspan=2)

    telefone_entries = []

    def adicionar_telefone(num="", tipo=""):
        frame = Frame(telefones_frame)
        frame.pack(pady=2)

        entry_num = Entry(frame, width=14)
        entry_num.insert(0, num)
        entry_num.pack(side=LEFT, padx=2)

        entry_tipo = Entry(frame, width=14)
        entry_tipo.insert(0, tipo)
        entry_tipo.pack(side=LEFT, padx=2)

        telefone_entries.append((entry_num, entry_tipo))

        btn_telefone = Button(tela, text="Adicionar Telefone", command=lambda: adicionar_telefone())
        btn_telefone.grid(row=len(labels)+2, column=0, columnspan=2, pady=5)

    for _, num, tipo in telefones:
        adicionar_telefone(num, tipo)

    def salvar_edicao():
        conn = sqlite3.connect('gestao_clientes.db')
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE clientes SET
                nome=?, idade=?, cpf=?, email=?, endereco=?, localidade=?, data_nascimento=?, status=?
            WHERE id=?
        """, (
            entry_nome.get(), entry_idade.get(), entry_cpf.get(), entry_email.get(),
            entry_endereco.get(), entry_localidade.get(), entry_data.get(),
            entry_status.get(), cliente_id
        ))

        cursor.execute("DELETE FROM cliente_telefones WHERE cliente_id=?", (cliente_id,))

        for num, tipo in telefone_entries:
            if num.get().strip():
                cursor.execute("""
                    INSERT INTO cliente_telefones (numeros, tipo, cliente_id)
                    VALUES (?, ?, ?)
                """, (num.get(), tipo.get(), cliente_id))

        conn.commit()
        conn.close()

        atualizar_tree()
        tela.destroy()

    Button(
        tela,
        text="Salvar Alterações",
        command=salvar_edicao
    ).grid(row=11, column=0, columnspan=2, pady=10)

#clique na tabela
def clique_na_tabela(event):
    item = tree.identify_row(event.y)
    coluna = tree.identify_column(event.x)

    if not item or coluna != "#5":
        return

    cliente_id = tree.item(item, "values")[0]

    x = event.x - tree.bbox(item, coluna)[0]

    texto = tree.item(item, "values")[4]

    metade = tree.column("acao", "width") // 2

    if x < metade:
        editar_cliente(cliente_id)
    else:
        deletar_cliente(cliente_id)

tree.bind("<Button-1>", clique_na_tabela)

#deletar cliente
def deletar_cliente(cliente_id):
    conn = sqlite3.connect('gestao_clientes.db')
    cursor = conn.cursor()

    cursor.execute("SELECT nome FROM clientes WHERE id=?", (cliente_id,))
    nome = cursor.fetchone()[0]

    resposta = messagebox.askyesno(
        "Confirmação",
        f"Deseja realmente deletar:\n\n{nome}?"
    )

    if resposta:
        cursor.execute("DELETE FROM clientes WHERE id=?", (cliente_id,))
        conn.commit()
        conn.close()
        atualizar_tree()


conn.commit()
janela.mainloop()
conn.close()

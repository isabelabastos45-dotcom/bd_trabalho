import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect('gestao_clientes.db')
cursor = conn.cursor()
cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("DROP TABLE IF EXISTS cliente_telefones;")
cursor.execute("DROP TABLE IF EXISTS clientes;")
conn.commit()

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
conn.commit()

def adicionar_cliente():
    def salvar():
        conn = sqlite3.connect('gestao_clientes.db')
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO clientes (nome, idade, cpf, email, endereco, localidade, data_nascimento, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entry_nome.get(), entry_idade.get(), entry_cpf.get(), entry_email.get(),
            entry_endereco.get(), entry_localidade.get(), entry_data.get(), entry_status.get()
        ))
        conn.commit()
        tree.insert("", END, values=(cursor.lastrowid, entry_nome.get(), entry_cpf.get(), entry_email.get(), "Editar"))
        tela.destroy()

    tela = Toplevel(janela)
    tela.title("Adicionar Cliente")

    labels = ["Nome","Idade","CPF","Email","Endereco","Localidade","Data Nascimento","Status"]
    entries = []

    for i,l in enumerate(labels):
        Label(tela,text=l).grid(row=i,column=0)
        e = Entry(tela); e.grid(row=i,column=1)
        entries.append(e)

    entry_nome,entry_idade,entry_cpf,entry_email,entry_endereco,entry_localidade,entry_data,entry_status = entries
    Button(tela,text="Salvar",command=salvar).grid(row=8,column=0,columnspan=2)

def editar_cliente():
    selecionado = tree.focus()
    if not selecionado:
        return

    cliente_id = tree.item(selecionado,'values')[0]

    conn = sqlite3.connect('gestao_clientes.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT nome, cpf, email, endereco, localidade, data_nascimento, status
    FROM clientes WHERE id=?
    """,(cliente_id,))
    dados = cursor.fetchone()

    def salvar_edicao():
        conn = sqlite3.connect('gestao_clientes.db')
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE clientes 
        SET nome=?, cpf=?, email=?, endereco=?, localidade=?, data_nascimento=?, status=?
        WHERE id=?
        """, (
            entry_nome.get(), entry_cpf.get(), entry_email.get(),
            entry_endereco.get(), entry_localidade.get(), entry_data.get(),
            entry_status.get(), cliente_id
        ))
        conn.commit()
        tree.item(selecionado,values=(cliente_id,entry_nome.get(),entry_cpf.get(),entry_email.get(),"Editar"))
        tela.destroy()

    tela = Toplevel(janela)
    tela.title("Editar Cliente")

    labels = ["Nome","CPF","Email","Endereco","Localidade","Data Nascimento","Status"]
    entries = []

    for i,l in enumerate(labels):
        Label(tela,text=l).grid(row=i,column=0)
        e = Entry(tela); e.grid(row=i,column=1)
        entries.append(e)

    entry_nome,entry_cpf,entry_email,entry_endereco,entry_localidade,entry_data,entry_status = entries

    for e,v in zip(entries,dados):
        e.insert(0,v)

    Button(tela,text="Salvar Alterações",command=salvar_edicao).grid(row=7,column=0,columnspan=2)

def clique_na_tabela(event):
    item = tree.identify_row(event.y)
    coluna = tree.identify_column(event.x)
    if coluna == '#5' and item:
        tree.selection_set(item)
        editar_cliente()

janela = Tk()
janela.title("Gestão de Clientes")

tree = ttk.Treeview(janela,columns=("c1","c2","c3","c4","c5"),show="headings")
tree.bind("<ButtonRelease-1>",clique_na_tabela)

for i,t in enumerate(["ID","Nome","CPF","Email","Ações"],1):
    tree.heading(f"#{i}",text=t)
    tree.column(f"#{i}",width=150)

tree.grid(row=0,column=0)

Button(janela,text="Adicionar Cliente",command=adicionar_cliente).grid(row=1,column=0,pady=10)

cursor.execute("SELECT id,nome,cpf,email FROM clientes")
for r in cursor.fetchall():
    tree.insert("",END,values=(r[0],r[1],r[2],r[3],"Editar"))
    
def deletar_cliente():
    selecionado = tree.focus()
    
    # Verifica se algum item foi selecionado
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um cliente para deletar.")
        return

    valores = tree.item(selecionado, 'values')
    cliente_id = valores[0]
    nome_cliente = valores[1]

    # Confirmação obrigatória
    resposta = messagebox.askyesno(
        "Confirmação",
        f"Você tem certeza que deseja deletar o cliente:\n\n{nome_cliente}?"
    )

    if resposta:
        conn = sqlite3.connect('gestao_clientes.db')
        cursor = conn.cursor()

        cursor.execute("""
        DELETE FROM clientes WHERE id = ?
        """, (cliente_id,))

        conn.commit()
        conn.close()

        # Remove da tabela visual
        tree.delete(selecionado)

        messagebox.showinfo("Sucesso", "Cliente deletado com sucesso.")
Button(janela, text="Deletar Cliente", command=deletar_cliente).grid(row=2, column=0, pady=10)


conn.close()
janela.mainloop()
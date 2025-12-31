import sqlite3

conn = sqlite3.connect('clientes.db')
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(150) NOT NULL,
    idade INTEGER,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    localidade VARCHAR(100),
    data_nascimento DATE,
    status INTEGER NOT NULL CHECK (status IN (0,1))
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cliente_telefones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero VARCHAR(20),
    tipo VARCHAR(100),
    cliente_id INTEGER,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);
""")

print("Tabelas criadas com sucesso")

conn.close()

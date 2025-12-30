import sqlite3

conn = sqlite3.connect('clientes.db') 

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE clientes (
        id INT PRIMARY KEY AUTOINCREMENT,
        nome VARCHAR(150) MANDATORY,
        idade INT,
        cpf     VARCHAR(11) UNIQUE MANDATORY,
        email VARCHAR(100) UNIQUE,
        localidade VARCHAR(100),
        data_nascimento DATE,
        status BOOLEAN
);
               
CREATE TABLE cliente_telefones (
        id PRIMARY KEY,
        numero VARCHAR(20),
        tipo VARCHAR(100),
        cliente_id FOREIGNER KEY
               )
""")

print('Tabela criada com sucesso.')

conn.close()



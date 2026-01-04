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
cursor.execute("""
INSERT INTO clientes (nome, idade, cpf, email, localidade, data_nascimento, status) 
VALUES ('Isabela Bento Bastos', 16, '12345678915', 'isabela.bento@gmail.com', 'Fortaleza', '2009-02-01', 1);
""")

cursor.execute("""
INSERT INTO clientes (nome, idade, cpf, email, localidade, data_nascimento, status) 
VALUES ('Júlia Lins de Alencar', 17, '12345678815', 'julia.lins@gmail.com', 'Fortaleza', '2009-02-02', 1);
""")

cursor.execute("""
INSERT INTO clientes (nome, idade, cpf, email, localidade, data_nascimento, status) 
VALUES ('Letícia Ozório de Lemos', 17, '12345678715', 'leticia.ozorio@gmail.com', 'Fortaleza', '2009-02-03', 1);
""")

cursor.execute("""
INSERT INTO clientes (nome, idade, cpf, email, localidade, data_nascimento, status) 
VALUES ('Loren Maria Félix Lessa', 17, '12345678615', 'loren.felix@gmail.com', 'Fortaleza', '2009-02-04', 1);
""")

cursor.execute("""
INSERT INTO clientes (nome, idade, cpf, email, localidade, data_nascimento, status) 
VALUES ('Mauricio Ferreira', 17, '12345679915', 'mauricio.ferreira@gmail.com','Fortaleza', '2009-02-05', 1);
""")

#adicionar informações em cliente_telefones
cursor.execute("""
INSERT INTO cliente_telefones (numero, tipo, cliente_id) 
VALUES ('111', 'Fixo', 1);
""")
cursor.execute("""
INSERT INTO cliente_telefones (numero, tipo, cliente_id) 
VALUES ('222', 'WhatsApp', 2);
""")

cursor.execute("""
INSERT INTO cliente_telefones (numero, tipo, cliente_id) 
VALUES ('333', 'Telefone', 3);
""")
cursor.execute("""
INSERT INTO cliente_telefones (numero, tipo, cliente_id) 
VALUES ('444', 'Fixo', 4);
""")

cursor.execute("""           
INSERT INTO cliente_telefones (numero, tipo, cliente_id) 
VALUES ('555', 'Telefone', 5);
""")

conn.commit()
conn.close()

print("Dados inseridos com sucesso")
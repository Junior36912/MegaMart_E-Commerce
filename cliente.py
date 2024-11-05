import sqlite3

conn = sqlite3.connect('vendas.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS cliente (
                idcliente INTEGER PRIMARY KEY,
                nome TEXT,
                email TEXT,
                telefone TEXT,
                data_nasc DATE,
                cidade TEXT,
                bairro TEXT,
                rua TEXT,
                numero_casa TEXT,
                senha TEXT
            )''')
conn.commit()

def listar_contatos():
    c.execute("SELECT * FROM cliente")
    print(c.fetchall())

def add_contato(nome1, email1, telefone1, data_nasc1, cidade1, bairro1, rua1, numero_casa1, senha1):
    c.execute("INSERT INTO cliente (nome, email, telefone, data_nasc, cidade, bairro, rua, numero_casa, senha) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (nome1, email1, telefone1, data_nasc1, cidade1, bairro1, rua1, numero_casa1, senha1))
    conn.commit()
    listar_contatos()

def delete(id_cliente1):
    c.execute("DELETE FROM cliente WHERE idcliente = ?", (id_cliente1,))
    conn.commit()
    listar_contatos()

def busca_por_id(id_cliente1):
    c.execute("SELECT * FROM cliente WHERE idcliente = ?", (id_cliente1,))
    resultado = c.fetchone()
    if resultado:
        print(resultado)
    else:
        print("Contato não encontrado")
        
        
add_contato("Harry Potter", "harry@example.com", "(11) 98765-4321", "1980-07-31", "Privet Drive", "Little Whinging", "Rua dos Alfeneiros", "4", "harry")
add_contato("Hermione Granger", "hermione@example.com", "(11) 98765-4322", "1979-09-19", "Timbuktu", "Bairro Central", "Rua dos Feiticeiros", "100", "herm")
add_contato("Frodo Bolseiro", "frodo@example.com", "(11) 98765-4323", "2968-09-22", "Condado", "Bairro Bolsão", "Rua do Anel", "1", "frodo")
add_contato("Katniss Everdeen", "katniss@example.com", "(11) 98765-4324", "2012-05-07", "Distrito 12", "Bairro Minerador", "Rua da Vitória", "13", "katniss")
add_contato("Sherlock Holmes", "sherlock@example.com", "(11) 98765-4325", "1854-01-06", "Baker Street", "Marylebone", "Rua Baker", "221B", "holmes")


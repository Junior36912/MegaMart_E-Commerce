import sqlite3
from datetime import date

conn = sqlite3.connect('vendas.db')
c = conn.cursor()

# Estrutura corrigida da tabela 'venda', de acordo com o que foi definido.
c.execute('''
          CREATE TABLE IF NOT EXISTS venda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_compra DATE NOT NULL,
            nome_cliente TEXT NOT NULL,
            endereco TEXT NOT NULL,
            metodo_pagamento TEXT NOT NULL,
            produto TEXT NOT NULL,
            valor REAL NOT NULL,
            quantidade INT
        );''')

def listar_vendas():
    c.execute("SELECT * FROM venda")
    print(c.fetchall())

# Corrigida a função de adicionar uma venda
def add_venda(data_compra, nome_cliente, endereco, metodo_pagamento, produto, valor, quantidade):
    conn = sqlite3.connect('vendas.db')
    c = conn.cursor()
    c.execute("INSERT INTO venda (data_compra, nome_cliente, endereco, metodo_pagamento, produto, valor, quantidade) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (data_compra, nome_cliente, endereco, metodo_pagamento, produto, valor, quantidade))
    conn.commit()
    conn.close()
    listar_vendas()

def delete_venda(id):
    conn = sqlite3.connect('vendas.db')
    c = conn.cursor()
    c.execute("DELETE FROM venda WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    listar_vendas()

def busca_venda_por_id(id):
    c.execute("SELECT * FROM venda WHERE id = ?", (id,))
    resultado = c.fetchone()
    if resultado:
        print(resultado)
    else:
        print("Venda não encontrada")

def editar_venda(id, data_compra, nome_cliente, endereco, metodo_pagamento, produto, valor, quantidade):
    conn = sqlite3.connect('vendas.db')
    c = conn.cursor()
    c.execute("UPDATE venda SET data_compra=?, nome_cliente=?, endereco=?, metodo_pagamento=?, produto=?, valor=?, quantidade=? WHERE id=?",
              (data_compra, nome_cliente, endereco, metodo_pagamento, produto, valor, id, quantidade))
    conn.commit()
    conn.close()

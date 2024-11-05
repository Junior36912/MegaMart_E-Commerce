import sqlite3

conn = sqlite3.connect('vendas.db')
c = conn.cursor()

c.execute('''DROP TABLE produto;''')

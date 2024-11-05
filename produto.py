import sqlite3

conn = sqlite3.connect('vendas.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS produto (
                idproduto INTEGER PRIMARY KEY,
                nome TEXT,
                preco REAL,
                marca TEXT,
                categoria TEXT,
                qtd INTEGER, 
                desc TEXT,
                img TEXT
            )''')
conn.commit()

def listar_produtos():
    c.execute("SELECT * FROM produto")
    print(c.fetchall())

def add_produto(nome, preco, marca, categoria, qtd, desc, img):
    c.execute("INSERT INTO produto (nome, preco, marca, categoria, qtd, desc, img) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (nome, preco, marca, categoria, qtd, desc, img))
    conn.commit()
    listar_produtos()

def delete_produto(id_produto):
    c.execute("DELETE FROM produto WHERE idproduto = ?", (id_produto,))
    conn.commit()
    listar_produtos()

def busca_produto_por_id(id_produto):
    c.execute("SELECT * FROM produto WHERE idproduto = ?", (id_produto,))
    resultado = c.fetchone()
    if resultado:
        print(resultado)
    else:
        print("Produto não encontrado")


add_produto("Camiseta Básica", 29.99, "Loja de Moda A", "Roupas", 100, "Camiseta branca básica feita com algodão, ideal para o dia a dia.", "https://github.com/Junior36912/imagens/blob/main/camisa_branca.jpg?raw=true")
add_produto("Tênis Esportivo", 89.99, "Loja de Calçados B", "Calçados", 50, "Tênis esportivo leve e confortável, ideal para corridas e caminhadas.", "https://github.com/Junior36912/imagens/blob/main/tenis_corrida.jpg?raw=true")
add_produto("Relógio Digital", 59.99, "Loja de Acessórios C", "Acessórios", 30, "Relógio digital com cronômetro, resistente à água.", "https://github.com/Junior36912/imagens/blob/main/relogio_digital.jpg?raw=true")
add_produto("Fone de Ouvido Bluetooth", 39.99, "Loja de Eletrônicos D", "Eletrônicos", 70, "Fone de ouvido Bluetooth com alta qualidade de som e bateria de longa duração.", "https://github.com/Junior36912/imagens/blob/main/Fone%20de%20Ouvido%20Bluetooth.jpg?raw=true")
add_produto("Cafeteira Elétrica", 149.99, "Loja de Eletrodomésticos E", "Eletrodomésticos", 20, "Cafeteira elétrica com capacidade para até 12 xícaras, design moderno.", "https://github.com/Junior36912/imagens/blob/main/Cafeteira%20El%C3%A9trica.jpg?raw=true")
add_produto("Livro de Receitas", 19.99, "Loja de Livros F", "Livros", 40, "Livro de receitas com mais de 100 pratos simples e rápidos de fazer.", "https://github.com/Junior36912/imagens/blob/main/Livro%20de%20Receitas.jpg?raw=true")
add_produto("Bicicleta Aro 26", 299.99, "Loja de Esportes G", "Esportes", 15, "Bicicleta Aro 26, ideal para trilhas e passeios urbanos.", "https://github.com/Junior36912/imagens/blob/main/Bicicleta%20Aro%2026.jpg?raw=true")
add_produto("Mochila Escolar", 49.99, "Loja de Acessórios H", "Acessórios", 60, "Mochila escolar resistente com vários compartimentos e design ergonômico.", "https://github.com/Junior36912/imagens/blob/main/Mochila%20Escolar.jpg?raw=true")
add_produto("Kit de Maquiagem", 34.99, "Loja de Beleza I", "Beleza", 25, "Kit completo de maquiagem com sombras, batons e blushes.", "https://github.com/Junior36912/imagens/blob/main/Kit%20de%20Maquiagem.png?raw=true")
add_produto("Smartphone Android", 699.99, "Loja de Eletrônicos J", "Eletrônicos", 10, "Smartphone Android com câmera dupla, 128GB de memória interna.", "https://github.com/Junior36912/imagens/blob/main/Smartphone%20Android.jpg?raw=true")
add_produto("Smartphone IPhone", 6699.99, "Loja de Eletrônicos J", "Eletrônicos", 10, "Smartphone iPhone de última geração com 256GB e câmera tripla.", "https://github.com/Junior36912/imagens/blob/main/Smartphone%20IPhone.jpg?raw=true")

# Produtos adicionais
add_produto("Mesa de Escritório", 199.99, "Loja de Móveis K", "Móveis", 8, "Mesa de escritório com design moderno, espaço para computador e acessórios.", "https://github.com/Junior36912/imagens/blob/main/mesa.jpeg?raw=true")
add_produto("Luminária de Mesa", 49.99, "Loja de Decoração L", "Decoração", 25, "Luminária de mesa com ajuste de brilho e design compacto.", "https://github.com/Junior36912/imagens/blob/main/luminaria.jpeg?raw=true")
add_produto("Caixa de Som Bluetooth", 79.99, "Loja de Eletrônicos M", "Eletrônicos", 40, "Caixa de som Bluetooth portátil com som estéreo de alta qualidade.", "https://github.com/Junior36912/imagens/blob/main/jbl.jpeg?raw=true")
add_produto("Cadeira Gamer", 499.99, "Loja de Móveis K", "Móveis", 12, "Cadeira gamer ergonômica com ajuste de altura e apoio para os braços.", "https://github.com/Junior36912/imagens/blob/main/cadeira_gamer.jpeg?raw=true")


add_produto("Tablet 10.1 Polegadas", 999.99, "Loja de Eletrônicos N", "Eletrônicos", 20, "Tablet com tela de 10.1 polegadas, 64GB de armazenamento e conexão 4G.", "https://github.com/Junior36912/imagens/blob/main/tablet.jpeg?raw=true")
add_produto("Aspirador de Pó", 299.99, "Loja de Eletrodomésticos O", "Eletrodomésticos", 15, "Aspirador de pó compacto com alto poder de sucção e filtro HEPA.", "https://github.com/Junior36912/imagens/blob/main/aspirador.jpeg?raw=true")
add_produto("Micro-ondas", 499.99, "Loja de Eletrodomésticos P", "Eletrodomésticos", 10, "Micro-ondas com painel digital, capacidade de 30 litros e várias funções de cozimento.", "https://github.com/Junior36912/imagens/blob/main/microondas.jpeg?raw=true")
add_produto("Monitor 24 Polegadas", 849.99, "Loja de Eletrônicos Q", "Eletrônicos", 25, "Monitor LED de 24 polegadas com resolução Full HD e tecnologia anti-reflexo.", "https://github.com/Junior36912/imagens/blob/main/monitor.jpeg?raw=true")
add_produto("Teclado Mecânico", 299.99, "Loja de Informática R", "Informática", 50, "Teclado mecânico com retroiluminação RGB, ideal para jogos e digitação rápida.", "https://github.com/Junior36912/imagens/blob/main/teclado.jpeg?raw=true")
add_produto("Mouse Gamer", 149.99, "Loja de Informática S", "Informática", 60, "Mouse gamer com sensor óptico de alta precisão e botões programáveis.", "https://github.com/Junior36912/imagens/blob/main/mouse.jpeg?raw=true")
add_produto("Batedeira Planetária", 399.99, "Loja de Eletrodomésticos T", "Eletrodomésticos", 20, "Batedeira planetária com 8 velocidades e tigela de aço inoxidável.", "https://github.com/Junior36912/imagens/blob/main/batedeira.jpeg?raw=true")
add_produto("Churrasqueira Elétrica", 249.99, "Loja de Eletrodomésticos U", "Eletrodomésticos", 12, "Churrasqueira elétrica portátil, ideal para ambientes pequenos.", "https://github.com/Junior36912/imagens/blob/main/churrasqueira-eletrica.jpeg?raw=true")
add_produto("Tênis Casual", 129.99, "Loja de Calçados V", "Calçados", 30, "Tênis casual confortável e versátil, perfeito para uso diário.", "https://github.com/Junior36912/imagens/blob/main/sapato.jpeg?raw=true")
add_produto("Jaqueta Jeans", 199.99, "Loja de Moda W", "Roupas", 40, "Jaqueta jeans unissex, estilo clássico com lavagem clara.", "https://github.com/Junior36912/imagens/blob/main/jaqueta_jeans.jpeg?raw=true")
add_produto("Óculos de Sol", 79.99, "Loja de Acessórios X", "Acessórios", 35, "Óculos de sol com proteção UV e lentes polarizadas.", "https://github.com/Junior36912/imagens/blob/main/oculos_sol.jpeg?raw=true")
add_produto("Skate Longboard", 249.99, "Loja de Esportes Y", "Esportes", 18, "Skate longboard com shape de madeira e rodas de alta resistência.", "https://github.com/Junior36912/imagens/blob/main/skate.jpeg?raw=true")
add_produto("Colchão Casal", 799.99, "Loja de Móveis Z", "Móveis", 5, "Colchão casal com molas ensacadas e revestimento em tecido antialérgico.", "https://github.com/Junior36912/imagens/blob/main/colchao.jpeg?raw=true")

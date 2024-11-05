import sqlite3
from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


app = Flask(__name__)
app.secret_key = "123"


# Inicializar o login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Define a página de login padrão


########################################################################################################################
########################################################################################################################
# SISTEMA DE LOGIN
class Usuario:
    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha

usuario1 = Usuario("0029", "123")
usuario2 = Usuario("0250", "123")
usuario3 = Usuario("0322", "123")

usuarios = { usuario1.nome : usuario1,
             usuario2.nome : usuario2,
             usuario3.nome : usuario3 }


# Classe User para login de gerentes (herda de UserMixin para compatibilidade com Flask-Login)
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Callback para carregar o usuário
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)



# Rota de login (GET) que renderiza a página de login com ou sem o formulário, dependendo do login
# Função para configurar o retorno de dados como dicionário
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Rota de login (GET)
@app.route('/login_geral')
def login_cliente():
    if 'usuario_logado' in session:
        return render_template('login_geral.html', usuario_logado=session['usuario_logado'])
    return render_template('login_geral.html')



# Rota de autenticação do cliente (POST)
@app.route('/autenticar_cliente', methods=['POST'])
def autenticar_cliente():
    nome = request.form['nome']
    senha = request.form['senha']
    
    # Conexão com o banco de dados
    banco = sqlite3.connect('vendas.db')
    banco.row_factory = dict_factory  # Configura o cursor para retornar dicionários
    cursor = banco.cursor()

    # Consulta para verificar o cliente
    cliente = cursor.execute('SELECT * FROM cliente WHERE nome = ? AND senha = ?', (nome, senha)).fetchone()

    if cliente:
        # Agora, cliente é um dicionário e podemos acessar pelo nome da coluna
        session['usuario_logado'] = cliente['nome']
        return redirect('/')
    else:
        return redirect('/login_geral')
    



# Rota de logout para o cliente
@app.route('/logout_cliente', methods=['POST'])
def logout_cliente():
    session.pop('usuario_logado', None)
    flash('Logout efetuado com sucesso!')
    return redirect('/')

@app.route('/sobre')
def sobre():
    return render_template('sobre.html') 

@app.route('/rota')
def rota():
    return render_template('your_template.html') 

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

from flask_login import login_user

@app.route('/autenticar', methods=['POST', 'GET'])
def autenticar():
    usuario = usuarios.get(request.form['usuario'])
    if usuario and usuario.senha == request.form['senha']:
        user = User(usuario.nome)  # Cria um objeto User
        login_user(user)  # Faz o login usando Flask-Login
        session['usuario_logado'] = usuario.nome
        flash(usuario.nome + ' logado com sucesso!')
        proxima_pagina = request.form.get('proxima')
        if proxima_pagina:
            return redirect('/catalogo_gerente')
        return redirect('/')
    flash('Usuário não logado.')
    return redirect(url_for('login'))




@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('login'))


########################################################################################################################
########################################################################################################################


@app.route('/')
def catalogo():
    # Conectar ao banco de dados
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()

    # Obter os parâmetros de ordenação e categoria da requisição (GET)
    sort_option = request.args.get('sort')
    categoria_option = request.args.get('categoria')

    # Definir a query base
    query = "SELECT * FROM produto"
    params = []

    # Modificar a query com base na categoria selecionada
    if categoria_option and categoria_option != 'todas':
        query += " WHERE categoria = ?"
        params.append(categoria_option)

    # Modificar a query com base na opção de ordenação
    if sort_option == 'nome_asc':
        query += " ORDER BY nome ASC"
    elif sort_option == 'nome_desc':
        query += " ORDER BY nome DESC"
    elif sort_option == 'preco_asc':
        query += " ORDER BY preco ASC"
    elif sort_option == 'preco_desc':
        query += " ORDER BY preco DESC"

    # Executar a query com ou sem parâmetros
    cursor.execute(query, params)
    produtos = cursor.fetchall()

    # Fechar a conexão com o banco de dados
    banco.close()

    # Renderizar a página com a lista de produtos filtrada e ordenada
    return render_template('catalogo.html', produtos=produtos)

@app.route('/catalogo_gerente')
@login_required
def catalogo_gerente():
    
    # Conectar ao banco de dados
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()

    # Obter os parâmetros de ordenação e categoria da requisição (GET)
    sort_option = request.args.get('sort')
    categoria_option = request.args.get('categoria')

    # Definir a query base
    query = "SELECT * FROM produto"
    params = []

    # Modificar a query com base na categoria selecionada
    if categoria_option and categoria_option != 'todas':
        query += " WHERE categoria = ?"
        params.append(categoria_option)

    # Modificar a query com base na opção de ordenação
    if sort_option == 'nome_asc':
        query += " ORDER BY nome ASC"
    elif sort_option == 'nome_desc':
        query += " ORDER BY nome DESC"
    elif sort_option == 'preco_asc':
        query += " ORDER BY preco ASC"
    elif sort_option == 'preco_desc':
        query += " ORDER BY preco DESC"

    # Executar a query com ou sem parâmetros
    cursor.execute(query, params)
    produtos = cursor.fetchall()

    # Fechar a conexão com o banco de dados
    banco.close()

    return render_template('catalogo_gerente.html', produtos=produtos)



# INFO PRODUTO

@app.route('/produto/<int:idproduto>')
def produto_info(idproduto):
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM produto WHERE idproduto = ?", (idproduto,))
    produto = cursor.fetchone()
    banco.close()

    if produto:
        return render_template('produto_info.html', produto=produto)
    else:
        return "Produto não encontrado", 404



@app.route('/adicionar_carrinho/<int:idproduto>', methods=['POST'])
def adicionar_carrinho(idproduto):
    banco = sqlite3.connect('vendas.db')
    banco.row_factory = dict_factory
    cursor = banco.cursor()
    produto = cursor.execute("SELECT * FROM produto WHERE idproduto = ?", (idproduto,)).fetchone()

    if produto:
        quantidade = int(request.form.get('quantidade', 1))  # Garantir que quantidade mínima é 1

        if quantidade > produto.get('qtd', 0):
            flash(f'Quantidade solicitada maior que o estoque disponível. Estoque atual: {produto["qtd"]}', 'danger')
            return redirect(url_for('produto_info', idproduto=idproduto))

        if 'carrinho' not in session:
            session['carrinho'] = []

        carrinho = session['carrinho']

        for item in carrinho:
            if 'idproduto' in item and item['idproduto'] == idproduto:
                if item['quantidade'] + quantidade > produto['qtd']:
                    flash(f'Quantidade total no carrinho excede o estoque. Estoque disponível: {produto["qtd"]}', 'danger')
                else:
                    item['quantidade'] += quantidade
                    flash(f'{produto["nome"]} foi atualizado no carrinho!', 'success')
                break
        else:
            carrinho.append({
                'idproduto': idproduto,
                'nome': produto['nome'],
                'preco': float(produto['preco']),
                'quantidade': quantidade
            })
            flash(f'{produto["nome"]} foi adicionado ao carrinho!', 'success')

        session['carrinho'] = carrinho
    else:
        flash('Produto não encontrado!', 'danger')

    return redirect(url_for('produto_info', idproduto=idproduto))





@app.route('/carrinho')
def ver_carrinho():
    carrinho = session.get('carrinho', [])
    
    # Cálculo do total garantindo que preço e quantidade são valores numéricos
    total = sum(float(item['preco']) * int(item['quantidade']) for item in carrinho)
    
    # Obter o endereço do cliente logado
    usuario_logado = session.get('usuario_logado')
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("SELECT cidade, bairro, rua, numero_casa FROM cliente WHERE nome = ?", (usuario_logado,))
    endereco = cursor.fetchone()
    banco.close()

    endereco_dict = {
        'cidade': endereco[0],
        'bairro': endereco[1],
        'rua': endereco[2],
        'numero_casa': endereco[3]
    } if endereco else {
        'cidade': "Endereço não encontrado",
        'bairro': "",
        'rua': "",
        'numero_casa': ""
    }

    return render_template('carrinho.html', carrinho=carrinho, total=total, endereco=endereco_dict)



@app.route('/finalizar_carrinho', methods=['POST'])
def finalizar_carrinho():
    carrinho = session.get('carrinho', [])
   
    if not carrinho:
        flash('Seu carrinho está vazio!', 'danger')
        return redirect(url_for('ver_carrinho'))
   
    # Calcular o total antes de continuar
    total = sum(float(item['preco']) * int(item['quantidade']) for item in carrinho)
   
    # Obter o endereço do cliente logado
    usuario_logado = session.get('usuario_logado')
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("SELECT cidade, bairro, rua, numero_casa, nome FROM cliente WHERE nome = ?", (usuario_logado,))
    endereco = cursor.fetchone()
    banco.close()

    endereco_dict = {
        'cidade': endereco[0],
        'bairro': endereco[1],
        'rua': endereco[2],
        'numero_casa': endereco[3],
        'nome': endereco[4]
    } if endereco else {
        'cidade': "Endereço não encontrado",
        'bairro': "",
        'rua': "",
        'numero_casa': "",
        'nome' : ""
    }
   
    # Renderizar a página de finalização com o endereço e o carrinho
    return render_template('finalizar_compras.html', carrinho=carrinho, total=total, endereco=endereco_dict)



@app.route('/remover_item_carrinho/<int:idproduto>', methods=['POST'])
def remover_item_carrinho(idproduto):
    carrinho = session.get('carrinho', [])
    
    # Filtrar o item que será removido
    carrinho = [item for item in carrinho if item['idproduto'] != idproduto]
    
    # Atualizar o carrinho na sessão
    session['carrinho'] = carrinho
    flash('Item removido do carrinho!', 'success')
    
    return redirect(url_for('ver_carrinho'))



########################################################################################################################
########################################################################################################################
# FINALIZAR COMPRAS

@app.route('/finalizar_compra/<int:idproduto>', methods=['POST'])
def finalizar_compra(idproduto):
    quantidade_comprada = int(request.form['quantidade'])
    
    # Conectar ao banco de dados e buscar o produto
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM produto WHERE idproduto = ?", (idproduto,))
    produto = cursor.fetchone()

    # Verificar se o produto existe
    if produto:
        estoque_atual = produto[5]

        # Verificar se há quantidade suficiente no estoque
        if quantidade_comprada > estoque_atual:
            flash('Quantidade solicitada maior que o estoque disponível!', 'danger')
            return redirect(url_for('produto_info', idproduto=idproduto))

        # Atualizar a quantidade no estoque
        novo_estoque = estoque_atual - quantidade_comprada
        cursor.execute("UPDATE produto SET qtd = ? WHERE idproduto = ?", (novo_estoque, idproduto))
        banco.commit()

        # Calcular o total da compra
        total = quantidade_comprada * float(produto[2])

        # Criar um dicionário do item
        item = {
            'nome': produto[1],
            'quantidade': quantidade_comprada,
            'preco': float(produto[2])
        }

        # Adicionar o item à sessão do carrinho
        carrinho = session.get('carrinho', [])
        carrinho.append(item)
        session['carrinho'] = carrinho  # Atualiza a sessão do carrinho

        # Obter o endereço do cliente logado
        usuario_logado = session.get('usuario_logado')
        cursor.execute("SELECT cidade, bairro, rua, numero_casa, nome FROM cliente WHERE nome = ?", (usuario_logado,))
        endereco = cursor.fetchone()

        endereco_dict = {
            'cidade': endereco[0],
            'bairro': endereco[1],
            'rua': endereco[2],
            'numero_casa': endereco[3],
            'nome': endereco[4]
        } if endereco else {
            'cidade': "Endereço não encontrado",
            'bairro': "",
            'rua': "",
            'numero_casa': "",
            'nome': ""
        }

        banco.close()

        # Passar o carrinho, total e o endereço para o template
        return render_template('finalizar_compras.html', carrinho=carrinho, total=total, endereco=endereco_dict)
    else:
        banco.close()
        return "Produto não encontrado", 404



########################################################################################################################
########################################################################################################################
# COMPRA FINALIZADA

@app.route('/pagamento', methods=['POST'])
def pagamento():
    metodo_pagamento = request.form['pagamento']
    flash(f'Pagamento via {metodo_pagamento} realizado com sucesso!', 'success')
    
    return redirect(url_for('confirmar_compra'))  # Certifique-se de que a rota está correta

from datetime import date  # To record the sale date
from venda import add_venda


@app.route('/confirmar_compra', methods=['GET', 'POST'])
def confirmar_compra():
    if request.method == 'POST':
        # Obtenha os dados do carrinho da sessão
        carrinho = session.get('carrinho', [])
        
        # Calcular o total da compra
        total = sum(float(item['preco']) * int(item['quantidade']) for item in carrinho)
        metodo_pagamento = request.form.get('pagamento')

        # Obter o endereço do cliente logado
        usuario_logado = session.get('usuario_logado')
        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("SELECT cidade, bairro, rua, numero_casa, nome FROM cliente WHERE nome = ?", (usuario_logado,))
        endereco = cursor.fetchone()

        endereco_dict = {
            'cidade': endereco[0],
            'bairro': endereco[1],
            'rua': endereco[2],
            'numero_casa': endereco[3],
            'nome': endereco[4]
        } if endereco else {
            'cidade': "Endereço não encontrado",
            'bairro': "",
            'rua': "",
            'numero_casa': "",
            'nome': ""
        }

        # Inserir a venda no banco de dados
        for item in carrinho:
            cursor.execute("INSERT INTO venda (data_compra, nome_cliente, endereco, metodo_pagamento, produto, valor, quantidade) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (date.today(), endereco_dict['nome'], f"{endereco_dict['rua']}, {endereco_dict['numero_casa']}, {endereco_dict['bairro']}, {endereco_dict['cidade']}",
                            metodo_pagamento, item['nome'], item['preco'] * item['quantidade'], item['quantidade']))

        banco.commit()
        banco.close()

        # Limpar o carrinho após a finalização da compra
        session.pop('carrinho', None)

        # Renderizar o template com as informações da compra
        return render_template('compra_concluida.html', carrinho=carrinho, total=total, metodo_pagamento=metodo_pagamento, endereco=endereco_dict)

    return redirect(url_for('ver_carrinho'))




@app.route('/pesquisar_produto')
def pesquisar_produto():
    nome_produto = request.args.get('search_name', " ")  # Obtém o nome do produto ou insere um espaço em branco por padrão

    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()

    # Utiliza LOWER() para ignorar maiúsculas/minúsculas e busca por produtos sem diferenciar acentuação
    nome_produto = nome_produto.lower()  # Converte a pesquisa para minúsculas
    cursor.execute("SELECT * FROM produto WHERE LOWER(nome) LIKE ?", ('%' + nome_produto + '%',))
    
    produtos = cursor.fetchall()  # Retorna todos os produtos encontrados
    banco.close()

    if produtos:
        return render_template('catalogo.html', produtos=produtos)  # Renderiza uma página com a lista de produtos
    else:
        flash("Produto não encontrado", "danger")
        return render_template('produto_nao_encontrado.html')
    

@app.route('/pesquisar_produto_gerente')
def pesquisar_produto_gerente():
    nome_produto = request.args.get('search_name', " ")  # Obtém o nome do produto ou insere um espaço em branco por padrão

    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()

    # Utiliza LOWER() para ignorar maiúsculas/minúsculas e busca por produtos sem diferenciar acentuação
    nome_produto = nome_produto.lower()  # Converte a pesquisa para minúsculas
    cursor.execute("SELECT * FROM produto WHERE LOWER(nome) LIKE ?", ('%' + nome_produto + '%',))
    
    produtos = cursor.fetchall()  # Retorna todos os produtos encontrados
    banco.close()

    if produtos:
        return render_template('catalogo_gerente.html', produtos=produtos)  # Renderiza uma página com a lista de produtos
    else:
        flash("Produto não encontrado", "danger")
        return render_template('produto_nao_encontrado_gerente.html')


########################################################################################################################
########################################################################################################################
# Ver vend

@app.route('/ver_vendas')
@login_required  # Make sure the user is logged in
def ver_vendas():
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()

    # Fetch all sales
    cursor.execute("SELECT * FROM venda")
    vendas = cursor.fetchall()

    # Fetch the client names for better readability
    cursor.execute("SELECT idcliente, nome FROM cliente")
    clientes = {cliente[0]: cliente[1] for cliente in cursor.fetchall()}

    # Convert the third column (Valor Total) to float
    vendas = [(venda[0], venda[1], venda[2], venda[3], venda[4], venda[5], venda[6], venda[7]) for venda in vendas]

    banco.close()

    return render_template('ver_vendas.html', vendas=vendas, clientes=clientes)



########################################################################################################################
########################################################################################################################
# TABELA CLIENTES


def carregar_dados_clientes():
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM cliente")
    data_prod = cursor.fetchall()
    banco.close()
    flash('Dados Atualizado!')
    return data_prod


@app.route('/tab_cliente')
def raiz_clientes():
    data_prod = carregar_dados_clientes()
    return render_template('tabela_cliente.html', data=data_prod)


#PESQUISAR CLIENTES


@app.route('/pesquisar_cliente')
def pesquisar_cliente():
    id_cliente = request.args.get('search_id')
    if id_cliente:
        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM cliente WHERE idcliente = ?", (id_cliente,))
        cliente = cursor.fetchone()
        banco.close()

        if cliente:
            return render_template('detalhes_cliente.html', cliente=cliente)
        else:
            flash("Cliente não encontrado", "danger")
            return render_template('cliente_nao_encontrado.html')
    else:
        return redirect(url_for('raiz_clientes'))


#ADICIONAR CLIENTES


@app.route('/adicionar')
def add_usuario():
    return render_template('adicionar.html')


@app.route("/adicionar_2", methods=["POST"])
def rota_adicionar():
    nome1 = request.form["nome"]
    email1 = request.form["email"]
    telefone1 = request.form["telefone"]
    data_nasc1 = request.form["data_nasc"]
    cidade1 = request.form["cidade"]

    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("INSERT INTO cliente (nome, email, telefone, data_nasc, cidade) VALUES (?, ?, ?, ?, ?)",
                   (nome1, email1, telefone1, data_nasc1, cidade1))
    banco.commit()
    banco.close()

    flash("Dados adicionados com sucesso")
    data_prod = carregar_dados_clientes()
    return render_template('tabela_cliente.html', data=data_prod)


#EXCLUIR CLIENTES


@app.route('/excluir/<int:idcliente>', methods=["GET"])
def rota_excluir_cliente(idcliente):
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("DELETE FROM cliente WHERE idcliente = ?", (idcliente,))
    banco.commit()
    banco.close()
    flash("Dados deletados com sucesso")
    return redirect(url_for("raiz_clientes"))


#EDITAR CLIENTES


@app.route('/editar_cliente/<int:idcliente>', methods=['GET', 'POST'])
def rota_editar_cliente(idcliente):
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        data_nasc = request.form['data_nasc']
        cidade = request.form['cidade']

        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("UPDATE cliente SET nome=?, email=?, telefone=?, data_nasc=?, cidade=? WHERE idcliente=?",
                       (nome, email, telefone, data_nasc, cidade, idcliente))
        banco.commit()
        banco.close()

        flash("Cliente editado com sucesso", "success")
        return redirect(url_for('raiz_clientes'))
    else:
        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM cliente WHERE idcliente=?", (idcliente,))
        cliente = cursor.fetchone()
        banco.close()

        return render_template('editar_cliente.html', cliente=cliente)


########################################################################################################################
########################################################################################################################
# TABELA PRODUTOS:


def carregar_dados_produtos():
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM produto")
    data = cursor.fetchall()
    banco.close()
    return data



@app.route('/tab_produtos')
def raiz_produtos():
    data = carregar_dados_produtos()
    return render_template('tabela_prod.html', data=data)



# PESQUISANDO PRODUTOS:


@app.route('/pesquisar_produto_id')
def pesquisar_produto_id():
    id_produto = request.args.get('search_id')
    if id_produto:
        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM produto WHERE idproduto = ?", (id_produto,))
        produto = cursor.fetchone()
        banco.close()

        if produto:
            return render_template('detalhes_produto.html', produto=produto)
        else:
            flash("Produto não encontrado", "danger")
            return render_template('produto_nao_encontrado.html')
    else:
        return redirect(url_for('raiz_produtos'))


#ADICIONAR PRODUTO


@app.route('/adicionar_produto')
def add_produto():
    return render_template('adicionar_produto.html')


@app.route("/adicionar_2_produto", methods=["POST"])
def rota_adicionar_produto():
    nome1 = request.form["nome"]
    preco1 = request.form["preco"]
    marca1 = request.form["marca"]
    categoria1 = request.form["categoria"]
    qtd1 = request.form["qtd"]

    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("INSERT INTO produto (nome, preco, marca, categoria, qtd) VALUES (?, ?, ?, ?, ?)",
                   (nome1, preco1, marca1, categoria1, qtd1))
    banco.commit()
    banco.close()

    flash("Dados adicionados com sucesso", "warning")
    data = carregar_dados_produtos()
    return render_template('tabela_prod.html', data=data)


#EXCLUIR PRODUTO


@app.route('/excluir_produto/<int:idproduto>', methods=['GET', 'POST'])
def rota_excluir_produto(idproduto):
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    if request.method == 'GET':
        # Exibir página de confirmação
        cursor.execute("SELECT * FROM produto WHERE idproduto = ?", (idproduto,))
        produto = cursor.fetchone()
        banco.close()
        return render_template('excluir_produto.html', produto=produto)
    elif request.method == 'POST':
        cursor.execute("DELETE FROM produto WHERE idproduto = ?", (idproduto,))
        banco.commit()
        banco.close()
        flash("Dados deletados com sucesso", "warning")
        return redirect(url_for("catalogo_gerente"))


#EDITAR PRODUTO


@app.route('/editar_produto/<int:idproduto>', methods=['GET', 'POST'])
def rota_editar_produto(idproduto):
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        marca = request.form['marca']
        categoria = request.form['categoria']
        qtd = request.form['qtd']
        desc = request.form['desc']

        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("UPDATE produto SET nome=?, preco=?, marca=?, categoria=?, qtd=?, desc=? WHERE idproduto=?",
                       (nome, preco, marca, categoria, qtd, desc, idproduto))
        banco.commit()
        banco.close()

        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM produto")
        produtos = cursor.fetchall()
        banco.close()
        flash("Produto editado com sucesso", "success")
        return render_template('catalogo_gerente.html', produtos=produtos)

    else:
        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM produto WHERE idproduto=?", (idproduto,))
        produto = cursor.fetchone()
        banco.close()

        return render_template('editar_produto.html', produto=produto)


########################################################################################################################
########################################################################################################################
# TABELA VENDAS:


def carregar_dados_vendas():
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("SELECT * FROM venda")
    vendas = cursor.fetchall()
    banco.close()
    return vendas



@app.route('/tab_venda')
def raiz_venda():
    vendas = carregar_dados_vendas()
    return render_template('tabela_venda.html', data=vendas)


# PESQUISANDO VENDAS:


@app.route('/pesquisar_venda')
def pesquisar_venda():
    id_venda = request.args.get('search_id')
    if id_venda:
        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM venda WHERE idvenda = ?", (id_venda,))
        venda = cursor.fetchone()
        banco.close()

        if venda:
            return render_template('detalhes_venda.html', venda=venda)
        else:
            flash("Venda não encontrada", "danger")
            return render_template('venda_nao_encontrada.html')
    else:
        return redirect(url_for('raiz_venda'))



@app.route('/adicionar_venda')
def add_venda():
    return render_template('adicionar_venda.html')



# Rota para exibir o formulário de cadastro
@app.route('/cadastrar')
def cadastrar():
    return render_template('cadastrar.html')



# Rota para processar o cadastro do cliente
@app.route('/processar_cadastro', methods=['POST'])
def processar_cadastro():
    nome = request.form['nome']
    senha = request.form['senha']
    email = request.form['email']
    telefone = request.form['telefone']
    cidade = request.form['cidade']
    bairro = request.form['bairro']
    rua = request.form['rua']
    numero_casa = request.form['numero_casa']

    # Conectar ao banco de dados e inserir o novo cliente
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("INSERT INTO cliente (nome, senha, email, telefone, cidade, bairro, rua, numero_casa) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (nome, senha, email, telefone, cidade, bairro, rua, numero_casa))
    banco.commit()
    banco.close()

    flash("Cadastro realizado com sucesso!", "success")
    return redirect(url_for('login_cliente'))

# Rota para exibir o perfil do cliente logado
@app.route('/perfil_cliente')
def perfil_cliente():
    if 'usuario_logado' in session:
        usuario_logado = session['usuario_logado']

        # Conectar ao banco de dados e obter os dados do cliente logado
        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("SELECT nome, email, telefone, cidade, bairro, rua, numero_casa FROM cliente WHERE nome = ?", (usuario_logado,))
        cliente = cursor.fetchone()
        banco.close()

        return render_template('perfil_cliente.html', cliente=cliente)
    else:
        flash("Você precisa estar logado para acessar essa página.", "danger")
        return redirect(url_for('login_cliente'))

# Rota para atualizar as informações do cliente
@app.route('/atualizar_cliente', methods=['POST'])
def atualizar_cliente():
    nome = request.form['nome']
    email = request.form['email']
    telefone = request.form['telefone']
    cidade = request.form['cidade']
    bairro = request.form['bairro']
    rua = request.form['rua']
    numero_casa = request.form['numero_casa']

    # Atualizar os dados do cliente no banco de dados
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("""
        UPDATE cliente SET email = ?, telefone = ?, cidade = ?, bairro = ?, rua = ?, numero_casa = ?
        WHERE nome = ?
    """, (email, telefone, cidade, bairro, rua, numero_casa, nome))
    banco.commit()
    banco.close()

    flash("Informações atualizadas com sucesso!", "success")
    return redirect(url_for('perfil_cliente'))


#ADICIONAR VENDA


@app.route('/adicionar_venda_2', methods=['GET', 'POST'])
def rota_adicionar_venda():
    if request.method == 'POST':
        data_venda1 = request.form['data_venda']
        valor_total1 = request.form['valor_total']
        idcliente1 = request.form['idcliente']
        idproduto1 = request.form['idproduto']
        funcionario1 = request.form['funcionario']

        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute(
            "INSERT INTO venda (data_venda, valor_total, idcliente, idproduto, funcionario) VALUES (?, ?, ?, ?, ?)",
            (data_venda1, valor_total1, idcliente1, idproduto1, funcionario1))
        banco.commit()
        banco.close()

        flash('Venda adicionada com sucesso!', 'success')
        return redirect(url_for('raiz_venda'))
    return render_template('adicionar_venda.html')


#EXCLUIR VENDA


@app.route('/excluir_venda/<int:idvenda>', methods=['GET'])
def rota_excluir_venda(idvenda):
    banco = sqlite3.connect('vendas.db')
    cursor = banco.cursor()
    cursor.execute("DELETE FROM venda WHERE idvenda = ?", (idvenda,))
    banco.commit()
    banco.close()
    flash("Dados deletados com sucesso", "warning")
    return redirect(url_for("raiz_venda"))


# EDITAR VENDA


@app.route('/editar_venda/<int:idvenda>', methods=['GET', 'POST'])
def editar_venda(idvenda):
    if request.method == 'POST':
        data_venda = request.form['data_venda']
        valor_total = request.form['valor_total']
        idcliente = request.form['idcliente']
        idproduto = request.form['idproduto']
        funcionario = request.form['funcionario']

        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute(
            "UPDATE venda SET data_venda=?, valor_total=?, idcliente=?, idproduto=?, funcionario=? WHERE idvenda=?",
            (data_venda, valor_total, idcliente, idproduto, funcionario, idvenda))
        banco.commit()
        banco.close()

        flash("Venda editada com sucesso", "success")
        return redirect(url_for('raiz_venda'))
    else:
        banco = sqlite3.connect('vendas.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM venda WHERE idvenda=?", (idvenda,))
        venda = cursor.fetchone()
        banco.close()

        return render_template('editar_venda.html', venda=venda)



# FUNCIONAR O APP

if __name__ == '__main__':
    app.run(debug=True)
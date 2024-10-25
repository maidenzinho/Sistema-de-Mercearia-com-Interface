from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
URLBANCO = "mysql+pymysql://root@localhost/mercearia"
motor = create_engine(URLBANCO)
Base = declarative_base()
Sessao = sessionmaker(bind=motor)
sessao = Sessao()
class Categoria(Base):
    __tablename__ = 'categorias'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    
    produtos = relationship('Produto', back_populates='categoria')
class Produto(Base):
    __tablename__ = 'produtos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False)
    categoriaid = Column(Integer, ForeignKey('categorias.id'), nullable=False)
    
    categoria = relationship('Categoria', back_populates='produtos')
class Cliente(Base):
    __tablename__ = 'clientes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=False)
    
    vendas = relationship('Venda', back_populates='cliente')
class Venda(Base):
    __tablename__ = 'vendas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    produtoid = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    clienteid = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    quantidade = Column(Integer, nullable=False)
    
    produto = relationship('Produto')
    cliente = relationship('Cliente', back_populates='vendas')
def criartabelas():
    Base.metadata.create_all(motor)
def criarcategoria():
    nome = input("Digite o nome da categoria: ")
    categoria = Categoria(nome=nome)
    sessao.add(categoria)
    sessao.commit()
    print("Categoria criada com sucesso!")
def criarproduto():
    nome = input("Digite o nome do produto: ")
    preco = float(input("Digite o preço do produto: "))
    estoque = int(input("Digite a quantidade em estoque: "))
    categoriaid = int(input("Digite o ID da categoria: "))
    produto = Produto(nome=nome, preco=preco, estoque=estoque, categoriaid=categoriaid)
    sessao.add(produto)
    sessao.commit()
    print("Produto criado com sucesso!")
def criarcliente():
    nome = input("Digite o nome do cliente: ")
    email = input("Digite o e-mail do cliente: ")
    telefone = input("Digite o telefone do cliente: ")
    cliente = Cliente(nome=nome, email=email, telefone=telefone)
    sessao.add(cliente)
    sessao.commit()
    print("Cliente criado com sucesso!")
def criarvenda():
    produtoid = int(input("Digite o ID do produto: "))
    clienteid = int(input("Digite o ID do cliente: "))
    quantidade = int(input("Digite a quantidade: "))
    venda = Venda(produtoid=produtoid, clienteid=clienteid, quantidade=quantidade)
    sessao.add(venda)
    sessao.commit()
    print("Venda criada com sucesso!")
def listarprodutos():
    produtos = sessao.query(Produto).all()
    for produto in produtos:
        print(f"ID: {produto.id}, Nome: {produto.nome}, Preço: {produto.preco}, Estoque: {produto.estoque}")
def listarcategorias():
    categorias = sessao.query(Categoria).all()
    for categoria in categorias:
        print(f"ID: {categoria.id}, Nome: {categoria.nome}")

def listarclientes():
    clientes = sessao.query(Cliente).all()
    for cliente in clientes:
        print(f"ID: {cliente.id}, Nome: {cliente.nome}, Email: {cliente.email}, Telefone: {cliente.telefone}")

def listarvendas():
    vendas = sessao.query(Venda).all()
    for venda in vendas:
        print(f"ID: {venda.id}, Produto ID: {venda.produtoid}, Cliente ID: {venda.clienteid}, Quantidade: {venda.quantidade}")
def atualizarproduto():
    produtoid = int(input("Digite o ID do produto a ser atualizado: "))
    produto = sessao.query(Produto).get(produtoid)
    if produto:
        nome = input("Digite o novo nome do produto (ou deixe vazio para não alterar): ")
        preco = input("Digite o novo preço do produto (ou deixe vazio para não alterar): ")
        estoque = input("Digite o novo estoque do produto (ou deixe vazio para não alterar): ")
        if nome:
            produto.nome = nome
        if preco:
            produto.preco = float(preco)
        if estoque:
            produto.estoque = int(estoque)
        sessao.commit()
        print("Produto atualizado com sucesso!")
    else:
        print("Produto não encontrado!")
def atualizarcliente():
    clienteid = int(input("Digite o ID do cliente a ser atualizado: "))
    cliente = sessao.query(Cliente).get(clienteid)
    if cliente:
        nome = input("Digite o novo nome do cliente (ou deixe vazio para não alterar): ")
        email = input("Digite o novo e-mail do cliente (ou deixe vazio para não alterar): ")
        telefone = input("Digite o novo telefone do cliente (ou deixe vazio para não alterar): ")
        if nome:
            cliente.nome = nome
        if email:
            cliente.email = email
        if telefone:
            cliente.telefone = telefone
        sessao.commit()
        print("Cliente atualizado com sucesso!")
    else:
        print("Cliente não encontrado!")
def deletarproduto():
    produtoid = int(input("Digite o ID do produto a ser deletado: "))
    produto = sessao.query(Produto).get(produtoid)
    if produto:
        sessao.delete(produto)
        sessao.commit()
        print("Produto deletado com sucesso!")
    else:
        print("Produto não encontrado!")
def deletarcliente():
    clienteid = int(input("Digite o ID do cliente a ser deletado: "))
    cliente = sessao.query(Cliente).get(clienteid)
    if cliente:
        sessao.delete(cliente)
        sessao.commit()
        print("Cliente deletado com sucesso!")
    else:
        print("Cliente não encontrado!")
def menu():
    while True:
        print("\n--- Menu de Opções ---")
        print("1. Criar Categoria")
        print("2. Criar Produto")
        print("3. Criar Cliente")
        print("4. Criar Venda")
        print("5. Listar Produtos")
        print("6. Listar Categorias")
        print("7. Listar Clientes")
        print("8. Listar Vendas")
        print("9. Atualizar Produto")
        print("10. Atualizar Cliente")
        print("11. Deletar Produto")
        print("12. Deletar Cliente")
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            criarcategoria()
        elif opcao == '2':
            criarproduto()
        elif opcao == '3':
            criarcliente()
        elif opcao == '4':
            criarvenda()
        elif opcao == '5':
            listarprodutos()
        elif opcao == '6':
            listarcategorias()
        elif opcao == '7':
            listarclientes()
        elif opcao == '8':
            listarvendas()
        elif opcao == '9':
            atualizarproduto()
        elif opcao == '10':
            atualizarcliente()
        elif opcao == '11':
            deletarproduto()
        elif opcao == '12':
            deletarcliente()
criartabelas()
menu()

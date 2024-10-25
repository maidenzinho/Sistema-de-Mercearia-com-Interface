import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QFormLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QHBoxLayout, QLabel
)
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URLBANCO = "mysql+pymysql://root@localhost/mercearia"
motor = create_engine(URLBANCO)
Base = declarative_base()
Sessao = sessionmaker(bind=motor)
sessao = Sessao()

class Categoria(Base):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)

class Produto(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False)
    categoriaid = Column(Integer, ForeignKey('categorias.id'), nullable=False)

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    telefone = Column(String(20), nullable=False)

class Venda(Base):
    __tablename__ = 'vendas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    produtoid = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    clienteid = Column(Integer, ForeignKey('clientes.id'), nullable=False)
    quantidade = Column(Integer, nullable=False)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sistema CRUD')
        self.setGeometry(100, 100, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()

        self.categoria_ui()
        self.produto_ui()
        self.cliente_ui()
        self.venda_ui()

        self.central_widget.setLayout(self.layout)

    def categoria_ui(self):
        self.categoria_form_layout = QFormLayout()
        self.categoria_nome_input = QLineEdit()
        
        self.categoria_form_layout.addRow('Nome da Categoria:', self.categoria_nome_input)
        
        self.categoria_button_layout = QHBoxLayout()
        self.categoria_add_button = QPushButton('Adicionar Categoria')
        self.categoria_add_button.clicked.connect(self.adicionar_categoria)
        self.categoria_update_button = QPushButton('Atualizar Categoria')
        self.categoria_update_button.clicked.connect(self.atualizar_categoria)
        self.categoria_delete_button = QPushButton('Deletar Categoria')
        self.categoria_delete_button.clicked.connect(self.deletar_categoria)

        self.categoria_refresh_button = QPushButton('Atualizar Lista')
        self.categoria_refresh_button.clicked.connect(self.listar_categorias)

        self.categoria_button_layout.addWidget(self.categoria_add_button)
        self.categoria_button_layout.addWidget(self.categoria_update_button)
        self.categoria_button_layout.addWidget(self.categoria_delete_button)
        self.categoria_button_layout.addWidget(self.categoria_refresh_button)

        self.categoria_table = QTableWidget()
        self.categoria_table.setColumnCount(2)
        self.categoria_table.setHorizontalHeaderLabels(['ID', 'Nome'])
        self.categoria_table.cellClicked.connect(self.selecionar_categoria)
        
        self.layout.addLayout(self.categoria_form_layout)
        self.layout.addLayout(self.categoria_button_layout)
        self.layout.addWidget(self.categoria_table)
        
        self.listar_categorias()

    def produto_ui(self):
        self.produto_form_layout = QFormLayout()
        self.produto_nome_input = QLineEdit()
        self.produto_preco_input = QLineEdit()
        self.produto_estoque_input = QLineEdit()
        self.produto_categoria_input = QLineEdit()

        self.produto_form_layout.addRow('Nome do Produto:', self.produto_nome_input)
        self.produto_form_layout.addRow('Preço do Produto:', self.produto_preco_input)
        self.produto_form_layout.addRow('Estoque do Produto:', self.produto_estoque_input)
        self.produto_form_layout.addRow('ID da Categoria:', self.produto_categoria_input)

        self.produto_button_layout = QHBoxLayout()
        self.produto_add_button = QPushButton('Adicionar Produto')
        self.produto_add_button.clicked.connect(self.adicionar_produto)
        self.produto_update_button = QPushButton('Atualizar Produto')
        self.produto_update_button.clicked.connect(self.atualizar_produto)
        self.produto_delete_button = QPushButton('Deletar Produto')
        self.produto_delete_button.clicked.connect(self.deletar_produto)

        self.produto_refresh_button = QPushButton('Atualizar Lista')
        self.produto_refresh_button.clicked.connect(self.listar_produtos)

        self.produto_button_layout.addWidget(self.produto_add_button)
        self.produto_button_layout.addWidget(self.produto_update_button)
        self.produto_button_layout.addWidget(self.produto_delete_button)
        self.produto_button_layout.addWidget(self.produto_refresh_button)

        self.produto_table = QTableWidget()
        self.produto_table.setColumnCount(4)
        self.produto_table.setHorizontalHeaderLabels(['ID', 'Nome', 'Preço', 'Estoque'])
        self.produto_table.cellClicked.connect(self.selecionar_produto)

        self.layout.addLayout(self.produto_form_layout)
        self.layout.addLayout(self.produto_button_layout)
        self.layout.addWidget(self.produto_table)

        self.listar_produtos()

    def cliente_ui(self):
        self.cliente_form_layout = QFormLayout()
        self.cliente_nome_input = QLineEdit()
        self.cliente_email_input = QLineEdit()
        self.cliente_telefone_input = QLineEdit()

        self.cliente_form_layout.addRow('Nome do Cliente:', self.cliente_nome_input)
        self.cliente_form_layout.addRow('Email do Cliente:', self.cliente_email_input)
        self.cliente_form_layout.addRow('Telefone do Cliente:', self.cliente_telefone_input)

        self.cliente_button_layout = QHBoxLayout()
        self.cliente_add_button = QPushButton('Adicionar Cliente')
        self.cliente_add_button.clicked.connect(self.adicionar_cliente)
        self.cliente_update_button = QPushButton('Atualizar Cliente')
        self.cliente_update_button.clicked.connect(self.atualizar_cliente)
        self.cliente_delete_button = QPushButton('Deletar Cliente')
        self.cliente_delete_button.clicked.connect(self.deletar_cliente)

        self.cliente_refresh_button = QPushButton('Atualizar Lista')
        self.cliente_refresh_button.clicked.connect(self.listar_clientes)

        self.cliente_button_layout.addWidget(self.cliente_add_button)
        self.cliente_button_layout.addWidget(self.cliente_update_button)
        self.cliente_button_layout.addWidget(self.cliente_delete_button)
        self.cliente_button_layout.addWidget(self.cliente_refresh_button)

        self.cliente_table = QTableWidget()
        self.cliente_table.setColumnCount(4)
        self.cliente_table.setHorizontalHeaderLabels(['ID', 'Nome', 'Email', 'Telefone'])
        self.cliente_table.cellClicked.connect(self.selecionar_cliente)

        self.layout.addLayout(self.cliente_form_layout)
        self.layout.addLayout(self.cliente_button_layout)
        self.layout.addWidget(self.cliente_table)

        self.listar_clientes()

    def venda_ui(self):
        self.venda_form_layout = QFormLayout()
        self.venda_produto_input = QLineEdit()
        self.venda_cliente_input = QLineEdit()
        self.venda_quantidade_input = QLineEdit()

        self.venda_form_layout.addRow('ID do Produto:', self.venda_produto_input)
        self.venda_form_layout.addRow('ID do Cliente:', self.venda_cliente_input)
        self.venda_form_layout.addRow('Quantidade:', self.venda_quantidade_input)

        self.venda_button_layout = QHBoxLayout()
        self.venda_add_button = QPushButton('Adicionar Venda')
        self.venda_add_button.clicked.connect(self.adicionar_venda)
        self.venda_update_button = QPushButton('Atualizar Venda')
        self.venda_update_button.clicked.connect(self.atualizar_venda)
        self.venda_delete_button = QPushButton('Deletar Venda')
        self.venda_delete_button.clicked.connect(self.deletar_venda)

        self.venda_refresh_button = QPushButton('Atualizar Lista')
        self.venda_refresh_button.clicked.connect(self.listar_vendas)

        self.venda_button_layout.addWidget(self.venda_add_button)
        self.venda_button_layout.addWidget(self.venda_update_button)
        self.venda_button_layout.addWidget(self.venda_delete_button)
        self.venda_button_layout.addWidget(self.venda_refresh_button)

        self.venda_table = QTableWidget()
        self.venda_table.setColumnCount(4)
        self.venda_table.setHorizontalHeaderLabels(['ID', 'Produto ID', 'Cliente ID', 'Quantidade'])
        self.venda_table.cellClicked.connect(self.selecionar_venda)

        self.layout.addLayout(self.venda_form_layout)
        self.layout.addLayout(self.venda_button_layout)
        self.layout.addWidget(self.venda_table)

        self.listar_vendas()

    def adicionar_categoria(self):
        nome = self.categoria_nome_input.text()
        if nome:
            nova_categoria = Categoria(nome=nome)
            sessao.add(nova_categoria)
            sessao.commit()
            QMessageBox.information(self, 'Sucesso', 'Categoria adicionada com sucesso!')
            self.categoria_nome_input.clear()
            self.listar_categorias()
        else:
            QMessageBox.warning(self, 'Erro', 'O nome não pode ser vazio.')

    def atualizar_categoria(self):
        current_row = self.categoria_table.currentRow()
        if current_row >= 0:
            categoria_id = int(self.categoria_table.item(current_row, 0).text())
            categoria = sessao.query(Categoria).get(categoria_id)
            novo_nome = self.categoria_nome_input.text()
            if novo_nome:
                categoria.nome = novo_nome
                sessao.commit()
                QMessageBox.information(self, 'Sucesso', 'Categoria atualizada com sucesso!')
                self.listar_categorias()
            else:
                QMessageBox.warning(self, 'Erro', 'O nome não pode ser vazio.')
        else:
            QMessageBox.warning(self, 'Erro', 'Selecione uma categoria para atualizar.')

    def deletar_categoria(self):
        current_row = self.categoria_table.currentRow()
        if current_row >= 0:
            categoria_id = int(self.categoria_table.item(current_row, 0).text())
            categoria = sessao.query(Categoria).get(categoria_id)
            sessao.delete(categoria)
            sessao.commit()
            QMessageBox.information(self, 'Sucesso', 'Categoria deletada com sucesso!')
            self.listar_categorias()
        else:
            QMessageBox.warning(self, 'Erro', 'Selecione uma categoria para deletar.')

    def listar_categorias(self):
        self.categoria_table.setRowCount(0)
        categorias = sessao.query(Categoria).all()
        for categoria in categorias:
            row_position = self.categoria_table.rowCount()
            self.categoria_table.insertRow(row_position)
            self.categoria_table.setItem(row_position, 0, QTableWidgetItem(str(categoria.id)))
            self.categoria_table.setItem(row_position, 1, QTableWidgetItem(categoria.nome))

    def selecionar_categoria(self, row, column):
        categoria_nome = self.categoria_table.item(row, 1).text()
        self.categoria_nome_input.setText(categoria_nome)

    def adicionar_produto(self):
        nome = self.produto_nome_input.text()
        preco = self.produto_preco_input.text()
        estoque = self.produto_estoque_input.text()
        categoriaid = self.produto_categoria_input.text()
        
        if nome and preco and estoque and categoriaid:
            novo_produto = Produto(nome=nome, preco=float(preco), estoque=int(estoque), categoriaid=int(categoriaid))
            sessao.add(novo_produto)
            sessao.commit()
            QMessageBox.information(self, 'Sucesso', 'Produto adicionado com sucesso!')
            self.produto_nome_input.clear()
            self.produto_preco_input.clear()
            self.produto_estoque_input.clear()
            self.produto_categoria_input.clear()
            self.listar_produtos()
        else:
            QMessageBox.warning(self, 'Erro', 'Todos os campos devem ser preenchidos.')

    def atualizar_produto(self):
        current_row = self.produto_table.currentRow()
        if current_row >= 0:
            produto_id = int(self.produto_table.item(current_row, 0).text())
            produto = sessao.query(Produto).get(produto_id)
            novo_nome = self.produto_nome_input.text()
            novo_preco = self.produto_preco_input.text()
            novo_estoque = self.produto_estoque_input.text()
            categoriaid = self.produto_categoria_input.text()

            if novo_nome and novo_preco and novo_estoque and categoriaid:
                produto.nome = novo_nome
                produto.preco = float(novo_preco)
                produto.estoque = int(novo_estoque)
                produto.categoriaid = int(categoriaid)
                sessao.commit()
                QMessageBox.information(self, 'Sucesso', 'Produto atualizado com sucesso!')
                self.listar_produtos()
            else:
                QMessageBox.warning(self, 'Erro', 'Todos os campos devem ser preenchidos.')
        else:
            QMessageBox.warning(self, 'Erro', 'Selecione um produto para atualizar.')

    def deletar_produto(self):
        current_row = self.produto_table.currentRow()
        if current_row >= 0:
            produto_id = int(self.produto_table.item(current_row, 0).text())
            produto = sessao.query(Produto).get(produto_id)
            sessao.delete(produto)
            sessao.commit()
            QMessageBox.information(self, 'Sucesso', 'Produto deletado com sucesso!')
            self.listar_produtos()
        else:
            QMessageBox.warning(self, 'Erro', 'Selecione um produto para deletar.')

    def listar_produtos(self):
        self.produto_table.setRowCount(0)
        produtos = sessao.query(Produto).all()
        for produto in produtos:
            row_position = self.produto_table.rowCount()
            self.produto_table.insertRow(row_position)
            self.produto_table.setItem(row_position, 0, QTableWidgetItem(str(produto.id)))
            self.produto_table.setItem(row_position, 1, QTableWidgetItem(produto.nome))
            self.produto_table.setItem(row_position, 2, QTableWidgetItem(str(produto.preco)))
            self.produto_table.setItem(row_position, 3, QTableWidgetItem(str(produto.estoque)))

    def selecionar_produto(self, row, column):
        produto_nome = self.produto_table.item(row, 1).text()
        self.produto_nome_input.setText(produto_nome)
        self.produto_preco_input.setText(self.produto_table.item(row, 2).text())
        self.produto_estoque_input.setText(self.produto_table.item(row, 3).text())

        produto_id = int(self.produto_table.item(row, 0).text())
        produto = sessao.query(Produto).get(produto_id)
        self.produto_categoria_input.setText(str(produto.categoriaid))

    def adicionar_cliente(self):
        nome = self.cliente_nome_input.text()
        email = self.cliente_email_input.text()
        telefone = self.cliente_telefone_input.text()

        if nome and email and telefone:
            novo_cliente = Cliente(nome=nome, email=email, telefone=telefone)
            sessao.add(novo_cliente)
            sessao.commit()
            QMessageBox.information(self, 'Sucesso', 'Cliente adicionado com sucesso!')
            self.cliente_nome_input.clear()
            self.cliente_email_input.clear()
            self.cliente_telefone_input.clear()
            self.listar_clientes()
        else:
            QMessageBox.warning(self, 'Erro', 'Todos os campos devem ser preenchidos.')

    def atualizar_cliente(self):
        current_row = self.cliente_table.currentRow()
        if current_row >= 0:
            cliente_id = int(self.cliente_table.item(current_row, 0).text())
            cliente = sessao.query(Cliente).get(cliente_id)
            novo_nome = self.cliente_nome_input.text()
            novo_email = self.cliente_email_input.text()
            novo_telefone = self.cliente_telefone_input.text()

            if novo_nome and novo_email and novo_telefone:
                cliente.nome = novo_nome
                cliente.email = novo_email
                cliente.telefone = novo_telefone
                sessao.commit()
                QMessageBox.information(self, 'Sucesso', 'Cliente atualizado com sucesso!')
                self.listar_clientes()
            else:
                QMessageBox.warning(self, 'Erro', 'Todos os campos devem ser preenchidos.')
        else:
            QMessageBox.warning(self, 'Erro', 'Selecione um cliente para atualizar.')

    def deletar_cliente(self):
        current_row = self.cliente_table.currentRow()
        if current_row >= 0:
            cliente_id = int(self.cliente_table.item(current_row, 0).text())
            cliente = sessao.query(Cliente).get(cliente_id)
            sessao.delete(cliente)
            sessao.commit()
            QMessageBox.information(self, 'Sucesso', 'Cliente deletado com sucesso!')
            self.listar_clientes()
        else:
            QMessageBox.warning(self, 'Erro', 'Selecione um cliente para deletar.')

    def listar_clientes(self):
        self.cliente_table.setRowCount(0)
        clientes = sessao.query(Cliente).all()
        for cliente in clientes:
            row_position = self.cliente_table.rowCount()
            self.cliente_table.insertRow(row_position)
            self.cliente_table.setItem(row_position, 0, QTableWidgetItem(str(cliente.id)))
            self.cliente_table.setItem(row_position, 1, QTableWidgetItem(cliente.nome))
            self.cliente_table.setItem(row_position, 2, QTableWidgetItem(cliente.email))
            self.cliente_table.setItem(row_position, 3, QTableWidgetItem(cliente.telefone))

    def selecionar_cliente(self, row, column):
        cliente_nome = self.cliente_table.item(row, 1).text()
        self.cliente_nome_input.setText(cliente_nome)
        self.cliente_email_input.setText(self.cliente_table.item(row, 2).text())
        self.cliente_telefone_input.setText(self.cliente_table.item(row, 3).text())

    def adicionar_venda(self):
        produtoid = self.venda_produto_input.text()
        clienteid = self.venda_cliente_input.text()
        quantidade = self.venda_quantidade_input.text()

        if produtoid and clienteid and quantidade:
            nova_venda = Venda(produtoid=int(produtoid), clienteid=int(clienteid), quantidade=int(quantidade))
            sessao.add(nova_venda)
            sessao.commit()
            QMessageBox.information(self, 'Sucesso', 'Venda adicionada com sucesso!')
            self.venda_produto_input.clear()
            self.venda_cliente_input.clear()
            self.venda_quantidade_input.clear()
            self.listar_vendas()
        else:
            QMessageBox.warning(self, 'Erro', 'Todos os campos devem ser preenchidos.')

    def atualizar_venda(self):
        current_row = self.venda_table.currentRow()
        if current_row >= 0:
            venda_id = int(self.venda_table.item(current_row, 0).text())
            venda = sessao.query(Venda).get(venda_id)
            novo_produtoid = self.venda_produto_input.text()
            novo_clienteid = self.venda_cliente_input.text()
            nova_quantidade = self.venda_quantidade_input.text()

            if novo_produtoid and novo_clienteid and nova_quantidade:
                venda.produtoid = int(novo_produtoid)
                venda.clienteid = int(novo_clienteid)
                venda.quantidade = int(nova_quantidade)
                sessao.commit()
                QMessageBox.information(self, 'Sucesso', 'Venda atualizada com sucesso!')
                self.listar_vendas()
            else:
                QMessageBox.warning(self, 'Erro', 'Todos os campos devem ser preenchidos.')
        else:
            QMessageBox.warning(self, 'Erro', 'Selecione uma venda para atualizar.')

    def deletar_venda(self):
        current_row = self.venda_table.currentRow()
        if current_row >= 0:
            venda_id = int(self.venda_table.item(current_row, 0).text())
            venda = sessao.query(Venda).get(venda_id)
            sessao.delete(venda)
            sessao.commit()
            QMessageBox.information(self, 'Sucesso', 'Venda deletada com sucesso!')
            self.listar_vendas()
        else:
            QMessageBox.warning(self, 'Erro', 'Selecione uma venda para deletar.')

    def listar_vendas(self):
        self.venda_table.setRowCount(0)
        vendas = sessao.query(Venda).all()
        for venda in vendas:
            row_position = self.venda_table.rowCount()
            self.venda_table.insertRow(row_position)
            self.venda_table.setItem(row_position, 0, QTableWidgetItem(str(venda.id)))
            self.venda_table.setItem(row_position, 1, QTableWidgetItem(str(venda.produtoid)))
            self.venda_table.setItem(row_position, 2, QTableWidgetItem(str(venda.clienteid)))
            self.venda_table.setItem(row_position, 3, QTableWidgetItem(str(venda.quantidade)))

    def selecionar_venda(self, row, column):
        self.venda_produto_input.setText(self.venda_table.item(row, 1).text())
        self.venda_cliente_input.setText(self.venda_table.item(row, 2).text())
        self.venda_quantidade_input.setText(self.venda_table.item(row, 3).text())

if __name__ == '__main__':
    Base.metadata.create_all(motor)
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

from flask import Blueprint, render_template, redirect, url_for, flash, request
from loja import db
from loja.produtos.models import Produto
from loja.admin.models import Cliente
from flask_login import login_required

produtos = Blueprint('produtos', __name__)

@produtos.route('/produto', methods=['GET', 'POST'])
@login_required
def produto():
    if request.method == 'POST':
        descricao = request.form['descricao']
        preco = request.form.get('preco', type=float)
        image_url = request.form.get('image_url')
        categoriaId = request.form.get('categoriaId', type=int)

        novo_produto = Produto(
            descricao=descricao,
            preco=preco,
            image_url=image_url,
            categoriaId=categoriaId
        )
        db.session.add(novo_produto)
        db.session.commit()
        flash('Produto adicionado com sucesso!', 'success')
        return redirect(url_for('produtos.lista_produtos'))
    return render_template('produto.html')

@produtos.route('/categorias')
@login_required
def categorias():
    return render_template('categorias.html')

@produtos.route('/clientes')
@login_required
def clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

@produtos.route('/')
@login_required
def lista_produtos():
    produtos = Produto.query.all()
    return render_template('produtos.html', produtos=produtos)

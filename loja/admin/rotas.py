from flask import render_template, session, request, redirect, url_for, flash, Blueprint
from loja import db, bcrypt, login_manager
from loja.admin.forms import LoginForm, RegisterForm
from loja.admin.models import Role, Utilizador, Cliente
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps

admin = Blueprint('admin', __name__)

@login_manager.user_loader
def load_user(user_id):
    return Utilizador.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Favor fazer seu login no sistema primeiro', 'danger')
            return redirect(url_for('admin.login'))
        
        if current_user.roleId != 1:
            flash('Você não tem permissão para acessar esta página', 'danger')
            return redirect(url_for('admin.home')) 
        
        return f(*args, **kwargs)
    
    return decorated_function

@admin.route('/')
def layout():
    return render_template('layouts.html')

@admin.route('/home')
@login_required
def home():
    return render_template('admin/home.html')

@admin.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    return render_template('admin/index.html', title='Página Administrativa')

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin_dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Utilizador.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('admin/login.html', form=form)

@admin.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Utilizador(email=form.email.data, password=hashed_password, roleId=2)
        db.session.add(user)
        db.session.commit()

        cliente = Cliente(nome=form.nome.data, morada=form.morada.data, utilizadorId=user.id)
        db.session.add(cliente)
        db.session.commit()

        flash('Your account has been created!', 'success')
        return redirect(url_for('admin.login'))
    return render_template('admin/registrar.html', form=form)

@admin.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin.login'))

@admin.route('/clientes')
@login_required
def clientes():
    return render_template('clientes.html')

@admin.route('/produtos')
@login_required
def produtos():
    return render_template('produtos.html')

@admin.route('/categorias')
@login_required
def categorias():
    return render_template('categorias.html')

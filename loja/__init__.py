from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ty4425hk54a21eee5719b9s9df7sdfklx'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:3242@localhost:3306/shopdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'admin.login'
    login_manager.login_message_category = 'info'

    from loja.admin.rotas import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from loja.produtos.rotas import produtos as produtos_blueprint
    app.register_blueprint(produtos_blueprint, url_prefix='/produtos')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

from loja import app, db
from loja.admin import rotas as admin_rotas  
from loja.produtos import rotas as produtos_rotas  


app.register_blueprint(admin_rotas.admin_bp)
app.register_blueprint(produtos_rotas.produtos_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all() 
    app.run(debug=True)


from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager # Este es para manejar sesiones de usuario (login/logout)
from backend.auth.routes import auth_bp # Traemos las rutas organizadas por modulos. ej, en la carpeta auth trame el modulo routes e importamos auth_bp
from backend.admin.routes import admin_bp  # Traems las rutas organizadas por modulos, aca entramos en la carpeta admin y en el archivo routes.py y le pedimos que importe la ruta admin_bp
from backend.cliente.routes import cliente_bp, inventario_bp # aca entramos en la carpeta cliente y en el archivo routes e importamos cliente_bp
from backend.database.instance.database import db # aca conectamos con la instancia de la base de datos. la carpeta database, carpeta instance y la base de datos, importamos db.
from backend.admin.models import Administrador # aca entramos en admin, en el archivo models e importamos la clase Administrador
from backend.cliente.models import Usuario # aca entramos en la carpeta cliente, archivo models e importamos la clase Usuario
import os # os usamos para trabajar con rutas de archivos

from backend.cliente.models import Producto



# Inicializamos la app Flask
app = Flask(__name__, template_folder='templates')  # Aca le especificamos la carpeta templates

# Configuramos el URI de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'database/instance/database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'clave-secreta-mas-segura'  # Cambia esto por una clave segura

# Inicializamos login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login_cliente'

# Definimos el user_loader mejorado
@login_manager.user_loader
def load_user(user_id): #definimos un parametro (user_id) user es una variable el cual vamos a darle el valor que encuentre en la tabla Administrador si es que encuentra algo con el identidicador que le da el usuario.
    user = Administrador.query.get(int(user_id))
    if user is None: # si no encuentra le decimos que busque en la otra tabla.
        user = Usuario.query.get(int(user_id))
    return user

# Inicializamos la base de datos
db.init_app(app)

# Registramos los blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(inventario_bp)

# Ruta principal
@app.route('/')
def home():
    return render_template('cliente/index.html')  # Ruta correcta al index

# Ruta pública principal para administración
@app.route('/administracion')
def administracion():
    return render_template('admin/sesion_administracion.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
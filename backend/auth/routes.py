from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from flask_login import login_user, logout_user, current_user
from backend.admin.models import Administrador
from backend.cliente.models import Usuario




auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/logout')
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('auth.login_cliente'))

@auth_bp.route('/login_cliente', methods=['GET', 'POST'])
def login_cliente():
    if request.method == 'POST':
        usuario_usuario = request.form.get('usuario_usuario')
        password_usuario = request.form.get('password_usuario')

        usuario = Usuario.query.filter_by(usuario_usuario=usuario_usuario).first()
        
        if not usuario or usuario.password_usuario != password_usuario:
            return render_template('cliente/index.html', error_login='Usuario o contraseña incorrecto')
            return redirect(url_for('auth.login_cliente'))

        login_user(usuario)
        return redirect(url_for('cliente.perfil'))

    return render_template('cliente/index.html')

@auth_bp.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if current_user.is_authenticated and isinstance(current_user._get_current_object(), Administrador):
        return redirect(url_for('admin.perfil_administracion'))
    
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')

        admin = Administrador.query.filter_by(usuario=usuario).first()

        if not admin or admin.password != password:
            return render_template('admin/sesion_administracion.html', error_login='Usuario o contraseña incorrecto')
            return redirect(url_for('auth.login_admin'))

        login_user(admin)
        return redirect(url_for('admin.perfil_administracion'))

    return render_template('admin/sesion_administracion.html')


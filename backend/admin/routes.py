from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from backend.cliente.models import Usuario
from backend.database.instance.database import db
from backend.admin.models import Administrador

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/perfil_administracion')
@login_required
def perfil_administracion():
    if not isinstance(current_user._get_current_object(), Administrador):
        flash('Acceso no autorizado', 'error')
        return redirect(url_for('auth.login_admin'))
    return render_template('admin/perfil_administracion.html')

@admin_bp.route('/crear_usuario', methods=['POST'])
@login_required
def crear_usuario():
    if not isinstance(current_user._get_current_object(), Administrador):
        flash('No tienes permisos para esta acción', 'error')
        return redirect(url_for('auth.login_admin'))
    
    try:
        nuevo_usuario = Usuario(
            nombre_usuario=request.form['nombre_usuario'],
            telefono_usuario=request.form['telefono_usuario'],
            direccion_usuario=request.form['direccion_usuario'],
            usuario_usuario=request.form['usuario_usuario'],
            password_usuario=request.form['password_usuario']
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario creado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al crear usuario: {str(e)}', 'error')
    
    return redirect(url_for('admin.perfil_administracion'))

# ELIMINA las rutas login y logout de aquí (deben estar solo en auth)
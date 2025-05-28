from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from backend.cliente.models import Producto
from backend.database.instance.database import db
import os
from backend import app


cliente_bp = Blueprint('cliente', __name__, url_prefix='/cliente')

# Ruta del perfil de usuario
@cliente_bp.route('/perfil')
@login_required
def perfil():
    # Aquí podemos pasar información del usuario actual (current_user) a la plantilla
    return render_template('cliente/perfil.html', usuario=current_user)



# Unificamos las vistas de inventario y metemos prodcutos adentro para que se muestren una vez que haya cargados
@cliente_bp.route('/inventario')
@login_required
def inventario():
    productos = Producto.query.all()
    return render_template('cliente/inventario.html', usuario=current_user, productos=productos)



@cliente_bp.route('/crear_producto', methods=['GET'])
@login_required
def crear_producto():
    return render_template('cliente/crear-producto.html')






inventario_bp = Blueprint('inventario', __name__)

@inventario_bp.route('/inventario', methods=['POST'])
def guardar_producto():
    nombre = request.form['nombre_producto']
    referencia_interna = request.form['referencia_interna']
    referencia_fabricante = request.form['referencia_fabricante']
    categoria = request.form['categoria']
    tipo_producto = request.form['tipo_producto']
    unidad_medida = request.form['unidad_medida']
    precio_compra = request.form['precio_compra']
    impuesto_compra = request.form['impuesto_compra']
    proveedor = request.form['proveedor']
    precio_venta = request.form['precio_venta']
    impuesto_venta = request.form['impuesto_venta']
    cantidad_disponible = request.form.get('cantidad_disponible', 0)
    almacen = request.form['almacen']
    ubicacion = request.form['ubicacion']
    descripcion = request.form['notas']

    # Procesar imagen si se subió
    imagen = request.files['imagen']
    if imagen and imagen.filename != '':
        filename = secure_filename(imagen.filename)
        ruta_imagen = os.path.join('static/uploads', filename)
        imagen.save(ruta_imagen)
    else:
        ruta_imagen = None

# Esto es lo nuevo para mostrar en la interfaz
    if ruta_imagen:
        mostrar = ruta_imagen
    else:
        mostrar = "No hay imagen"


    # Crear producto y guardar
    producto = Producto(
        nombre=nombre,
        referencia_interna=referencia_interna,
        referencia_fabricante=referencia_fabricante,
        categoria=categoria,
        tipo_producto=tipo_producto,
        unidad_medida=unidad_medida,
        precio_compra=float(precio_compra),
        impuesto_compra=impuesto_compra,
        proveedor=proveedor,
        precio_venta=float(precio_venta),
        impuesto_venta=impuesto_venta,
        cantidad_disponible=int(cantidad_disponible),
        almacen=almacen,
        ubicacion=ubicacion,
        imagen= 'uploads/' + filename,
        descripcion=descripcion
    )

    db.session.add(producto)
    db.session.commit()

    return render_template('cliente/inventario.html')






@cliente_bp.route('/eliminar_producto/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    producto = Producto.query.filter_by(id = id).first()
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for('cliente.inventario'))


@cliente_bp.route('/editar_producto/<int:id>', methods=['GET'])
@login_required
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    return render_template('cliente/editar_producto.html', producto=producto)

@cliente_bp.route('/actualizar_producto/<int:id>', methods=['POST'])
@login_required
def actualizar_producto(id):
    producto = Producto.query.get_or_404(id)
    
    # Actualizar campos básicos
    producto.nombre = request.form.get('nombre')
    producto.referencia_interna = request.form.get('referencia_interna')
    producto.precio_venta = float(request.form.get('precio_venta', 0))
    producto.cantidad_disponible = int(request.form.get('cantidad_disponible', 0))
    
    # Manejo de la imagen
    if 'imagen' in request.files:
        imagen = request.files['imagen']
        if imagen.filename != '':
            filename = secure_filename(imagen.filename)
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            producto.imagen = 'uploads/' + filename
    
    db.session.commit()
    flash('Producto actualizado correctamente', 'success')
    return redirect(url_for('cliente.inventario'))

from backend.database.instance.database import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(50))
    telefono_usuario = db.Column(db.String(20))
    direccion_usuario = db.Column(db.String(100))
    usuario_usuario = db.Column(db.String(50), unique=True)
    password_usuario = db.Column(db.String(50))
    
    


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)  # Obligatorio

    # Datos generales
    referencia_interna = db.Column(db.String(100), nullable=True)
    referencia_fabricante = db.Column(db.String(100), nullable=True)
    categoria = db.Column(db.String(100), nullable=True)
    tipo_producto = db.Column(db.String(50), nullable=True)  # consumible, servicio, almacenable
    unidad_medida = db.Column(db.String(50), nullable=True)  # uom, kg, l

    # Compra
    precio_compra = db.Column(db.Float, nullable=True)
    impuesto_compra = db.Column(db.String(50), nullable=True)  # Puede ser 'IVA 10%', etc.
    proveedor = db.Column(db.String(100), nullable=True)

    # Venta
    precio_venta = db.Column(db.Float, nullable=True)
    impuesto_venta = db.Column(db.String(50), nullable=True)

    # Inventario
    cantidad_disponible = db.Column(db.Float, nullable=True)  # Esto puede ser 0 por defecto
    almacen = db.Column(db.String(100), nullable=True)
    ubicacion = db.Column(db.String(100), nullable=True)

    # Imagen
    imagen = db.Column(db.String, nullable=True)  # para guardar imagen en binario

    # Notas
    descripcion = db.Column(db.Text, nullable=True)

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# --- BASE DE DATOS PRODUCTOS ---

def get_db_connection_productos():
    conn = sqlite3.connect('productos.db')
    conn.row_factory = sqlite3.Row
    return conn

def crear_tabla_productos():
    conn = get_db_connection_productos()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            cantidad INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

crear_tabla_productos()

# --- BASE DE DATOS CLIENTES ---

def get_db_connection_clientes():
    conn = sqlite3.connect('clientes.db')
    conn.row_factory = sqlite3.Row
    return conn

def crear_tabla_clientes():
    conn = get_db_connection_clientes()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_compra TEXT NOT NULL,
            nombre TEXT NOT NULL,
            celular TEXT,
            domicilio TEXT,
            producto TEXT,
            cuotas_totales INTEGER,
            cuotas_pagadas INTEGER,
            estado_deuda TEXT
        )
    ''')
    conn.commit()
    conn.close()

crear_tabla_clientes()

# --- RUTAS PRODUCTOS ---

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/productos')
def productos():
    conn = get_db_connection_productos()
    productos = conn.execute('SELECT * FROM productos').fetchall()
    conn.close()
    return render_template('productos.html', productos=productos)

@app.route('/agregar_producto', methods=['POST'])
def agregar_producto():
    nombre = request.form['nombre']
    descripcion = request.form.get('descripcion', '')
    cantidad = request.form.get('cantidad', 0)
    try:
        cantidad = int(cantidad)
    except:
        cantidad = 0

    conn = get_db_connection_productos()
    conn.execute('INSERT INTO productos (nombre, descripcion, cantidad) VALUES (?, ?, ?)',
                 (nombre, descripcion, cantidad))
    conn.commit()
    conn.close()
    return redirect(url_for('productos'))

@app.route('/eliminar_producto/<int:id>', methods=['POST'])
def eliminar_producto(id):
    conn = get_db_connection_productos()
    conn.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('productos'))

# --- RUTAS CLIENTES ---

@app.route('/clientes')
def clientes():
    conn = get_db_connection_clientes()
    clientes = conn.execute('SELECT * FROM clientes').fetchall()
    conn.close()
    return render_template('clientes.html', clientes=clientes)

@app.route('/agregar_cliente', methods=['POST'])
def agregar_cliente():
    fecha_compra = request.form['fecha_compra']
    nombre = request.form['nombre']
    celular = request.form.get('celular')
    domicilio = request.form.get('domicilio')
    producto = request.form.get('producto')
    cuotas_totales = request.form.get('cuotas_totales')
    cuotas_pagadas = request.form.get('cuotas_pagadas')
    estado_deuda = request.form.get('estado_deuda', 'al_dia')

    try:
        cuotas_totales = int(cuotas_totales)
    except (ValueError, TypeError):
        cuotas_totales = 0

    try:
        cuotas_pagadas = int(cuotas_pagadas)
    except (ValueError, TypeError):
        cuotas_pagadas = 0

    conn = get_db_connection_clientes()
    conn.execute('''
        INSERT INTO clientes
        (fecha_compra, nombre, celular, domicilio, producto, cuotas_totales, cuotas_pagadas, estado_deuda)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (fecha_compra, nombre, celular, domicilio, producto, cuotas_totales, cuotas_pagadas, estado_deuda))
    conn.commit()
    conn.close()
    return redirect(url_for('clientes'))

@app.route('/editar_cliente/<int:id>')
def editar_cliente(id):
    conn = get_db_connection_clientes()
    cliente = conn.execute('SELECT * FROM clientes WHERE id = ?', (id,)).fetchone()
    conn.close()
    if cliente is None:
        return 'Cliente no encontrado', 404
    return render_template('editar_cliente.html', cliente=cliente)

@app.route('/actualizar_cliente/<int:id>', methods=['POST'])
def actualizar_cliente(id):
    fecha_compra = request.form['fecha_compra']
    nombre = request.form['nombre']
    celular = request.form.get('celular')
    domicilio = request.form.get('domicilio')
    producto = request.form.get('producto')
    cuotas_totales = request.form.get('cuotas_totales')
    cuotas_pagadas = request.form.get('cuotas_pagadas')
    estado_deuda = request.form.get('estado_deuda', 'al_dia')

    try:
        cuotas_totales = int(cuotas_totales)
    except (ValueError, TypeError):
        cuotas_totales = 0

    try:
        cuotas_pagadas = int(cuotas_pagadas)
    except (ValueError, TypeError):
        cuotas_pagadas = 0

    conn = get_db_connection_clientes()
    conn.execute('''
        UPDATE clientes SET
        fecha_compra = ?, nombre = ?, celular = ?, domicilio = ?, producto = ?,
        cuotas_totales = ?, cuotas_pagadas = ?, estado_deuda = ?
        WHERE id = ?
    ''', (fecha_compra, nombre, celular, domicilio, producto, cuotas_totales, cuotas_pagadas, estado_deuda, id))
    conn.commit()
    conn.close()
    return redirect(url_for('clientes'))

if __name__ == '__main__':
    app.run(debug=True)

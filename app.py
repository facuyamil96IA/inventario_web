from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)
DB = 'inventario.db'

def init_db():
    if not os.path.exists(DB):
        conn = sqlite3.connect(DB)
        conn.execute("""
            CREATE TABLE productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                precio REAL,
                cantidad INTEGER
            )
        """)
        conn.commit()
        conn.close()
        print("Base de datos creada automáticamente.")

init_db()

def get_db_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/productos')
def productos():
    q = request.args.get('q', '').strip()
    conn = get_db_connection()
    cursor = conn.cursor()
    if q:
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%'+q+'%',))
    else:
        cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return render_template('productos.html', productos=productos)

@app.route('/agregar', methods=['POST'])
def agregar():
    nombre = request.form['nombre']
    precio = float(request.form['precio'])
    cantidad = int(request.form['cantidad'])
    conn = get_db_connection()
    conn.execute("INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?)", (nombre, precio, cantidad))
    conn.commit()
    conn.close()
    return redirect('/productos')

@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    nombre = request.form['nombre']
    precio = float(request.form['precio'])
    cantidad = int(request.form['cantidad'])
    conn = get_db_connection()
    conn.execute("UPDATE productos SET nombre=?, precio=?, cantidad=? WHERE id=?", (nombre, precio, cantidad, id))
    conn.commit()
    conn.close()
    return redirect('/productos')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM productos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/productos')

if __name__ == '__main__':
    app.run(debug=True)

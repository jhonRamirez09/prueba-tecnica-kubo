import sqlite3

DB_NAME = "tareas.db"

def obtener_conexion():
    conexion = sqlite3.connect(DB_NAME)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion

def crear_tablas():
    conexion = obtener_conexion()
    conexion.execute('''
    CREATE TABLE IF NOT EXISTS usuarios(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
    )
''')
    conexion.execute('''
    CREATE TABLE IF NOT EXISTS tareas(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuarios_id INTEGER NOT NULL,
    titulo TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    prioridad TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'PENDIENTE',
    eliminado INTEGER NOT NULL DEFAULT 0,
    fecha_limite TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuarios_id) REFERENCES usuarios(id)
    )
''')
    conexion.commit()
    conexion.close()
    
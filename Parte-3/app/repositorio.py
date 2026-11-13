from datetime import date
from app.database import obtener_conexion


def crear_usuario(nombre, email):
    conexion = obtener_conexion()
    try:
        cursor = conexion.execute("INSERT INTO usuarios (nombre, email) VALUES (?,?)",
                                  (nombre, email))
        conexion.commit()
        nuevo_id = cursor.lastrowid
    finally:
        conexion.close()
    return obtener_usuario_por_id(nuevo_id)


def obtener_usuario_por_id(id):
    conexion = obtener_conexion()
    fila = conexion.execute("SELECT * FROM usuarios WHERE id = ?", (id,)).fetchone()
    conexion.close()
    if fila is None:
        return None
    return dict(fila)


def obtener_usuario_por_email(email):
    conexion = obtener_conexion()
    fila = conexion.execute("SELECT * FROM usuarios WHERE email = ?", (email,)).fetchone()
    conexion.close()
    if fila is None:
        return None
    return dict(fila)


def _tarea_a_dict(fila):
    if fila is None:
        return None
    tarea = dict(fila)
    tarea["usuario_id"] = tarea.pop("usuarios_id")
    tarea.pop("eliminado")
    return tarea


# Busca una tarea por id; las borradas (eliminado = 1) se tratan como si no existieran
def obtener_tarea_por_id(id):
    conexion = obtener_conexion()
    fila = conexion.execute("SELECT * FROM tareas WHERE id = ? AND eliminado = 0", (id,)).fetchone()
    conexion.close()
    return _tarea_a_dict(fila)


def crear_tarea(titulo, descripcion, prioridad, fecha_limite, usuario_id):
    conexion = obtener_conexion()
    try:
        cursor = conexion.execute(
            "INSERT INTO tareas (titulo, descripcion, prioridad, fecha_limite, usuarios_id) VALUES (?,?,?,?,?)",
            (titulo, descripcion, prioridad, str(fecha_limite), usuario_id))
        conexion.commit()
        nuevo_id = cursor.lastrowid
    finally:
        conexion.close()
    return obtener_tarea_por_id(nuevo_id)


# Filtros opcionales: si llegan en None no se aplican. Paginacion con LIMIT y OFFSET
def listar_tareas(estado, prioridad, usuario_id, page, size):
    condiciones = "eliminado = 0 AND (? IS NULL OR estado = ?) AND (? IS NULL OR prioridad = ?) AND (? IS NULL OR usuarios_id = ?)"
    parametros = (estado, estado, prioridad, prioridad, usuario_id, usuario_id)
    offset = (page - 1) * size

    conexion = obtener_conexion()
    try:
        total = conexion.execute(f"SELECT COUNT(*) AS total FROM tareas WHERE {condiciones}",
                                 parametros).fetchone()["total"]
        filas = conexion.execute(f"SELECT * FROM tareas WHERE {condiciones} ORDER BY id LIMIT ? OFFSET ?",
                                 parametros + (size, offset)).fetchall()
    finally:
        conexion.close()
    return [_tarea_a_dict(fila) for fila in filas], total


def actualizar_tarea(id, titulo, descripcion, prioridad, fecha_limite):
    conexion = obtener_conexion()
    try:
        conexion.execute(
            "UPDATE tareas SET titulo = ?, descripcion = ?, prioridad = ?, fecha_limite = ? WHERE id = ? AND eliminado = 0",
            (titulo, descripcion, prioridad, str(fecha_limite), id))
        conexion.commit()
    finally:
        conexion.close()
    return obtener_tarea_por_id(id)


def cambiar_estado(id, estado):
    conexion = obtener_conexion()
    try:
        conexion.execute("UPDATE tareas SET estado = ? WHERE id = ? AND eliminado = 0", (estado, id))
        conexion.commit()
    finally:
        conexion.close()
    return obtener_tarea_por_id(id)

# Borrado logico: no borra la fila, la marca con eliminado = 1. Devuelve cuantas filas marco
def eliminar_tarea(id):
    conexion = obtener_conexion()
    try:
        cursor = conexion.execute("UPDATE tareas SET eliminado = 1 WHERE id = ? AND eliminado = 0", (id,))
        conexion.commit()
        marcadas = cursor.rowcount
    finally:
        conexion.close()
    return marcadas


def contar_por_estado():
    conexion = obtener_conexion()
    filas = conexion.execute(
        "SELECT estado, COUNT(*) AS cantidad FROM tareas WHERE eliminado = 0 GROUP BY estado").fetchall()
    conexion.close()
    return [dict(fila) for fila in filas]


def contar_por_usuario():
    conexion = obtener_conexion()
    filas = conexion.execute(
        "SELECT usuarios_id AS usuario_id, COUNT(*) AS cantidad FROM tareas WHERE eliminado = 0 GROUP BY usuarios_id").fetchall()
    conexion.close()
    return [dict(fila) for fila in filas]

def contar_vencidas():
    conexion = obtener_conexion()
    fila = conexion.execute(
        "SELECT COUNT(*) AS vencidas FROM tareas WHERE eliminado = 0 AND estado != 'HECHA' AND fecha_limite < ?",
        (str(date.today()),)).fetchone()
    conexion.close()
    return fila["vencidas"]
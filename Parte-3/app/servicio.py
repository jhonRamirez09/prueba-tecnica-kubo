from app import repositorio

class UsuarioNoEncontrado(Exception):
    pass

class EmailDuplicado(Exception):
    pass

class TareaNoEncontrada(Exception):
    pass

class TransicionInvalida(Exception):
    pass


ORDEN_ESTADOS = ["PENDIENTE", "EN_PROGRESO", "HECHA"]


def crear_usuario(nombre, email):
    nombre = nombre.strip()
    email = email.strip().lower()  
    if repositorio.obtener_usuario_por_email(email) is not None:
        raise EmailDuplicado(f"Ya existe un usuario con el email {email}")
    return repositorio.crear_usuario(nombre, email)


def obtener_usuario(id):
    usuario = repositorio.obtener_usuario_por_id(id)
    if usuario is None:
        raise UsuarioNoEncontrado(f"No existe el usuario con id {id}")
    return usuario


def obtener_tarea(id):
    tarea = repositorio.obtener_tarea_por_id(id)
    if tarea is None:
        raise TareaNoEncontrada(f"No existe la tarea con id {id}")
    return tarea


def crear_tarea(titulo, descripcion, prioridad, fecha_limite, usuario_id):
    obtener_usuario(usuario_id)
    return repositorio.crear_tarea(titulo.strip(), descripcion.strip(), prioridad, fecha_limite, usuario_id)


def listar_tareas(estado, prioridad, usuario_id, page, size):
    tareas, total = repositorio.listar_tareas(estado, prioridad, usuario_id, page, size)
    return {
        "items": tareas,
        "total": total,
        "page": page,
        "size": size
    }


def actualizar_tarea(id, titulo, descripcion, prioridad, fecha_limite):
    obtener_tarea(id)               # 404 si no existe o esta borrada
    return repositorio.actualizar_tarea(id, titulo.strip(), descripcion.strip(), prioridad, fecha_limite)


def cambiar_estado(id, nuevo_estado):
    tarea = obtener_tarea(id)
    actual = tarea["estado"]
    if ORDEN_ESTADOS.index(nuevo_estado) <= ORDEN_ESTADOS.index(actual):
        raise TransicionInvalida(f"No se puede pasar de {actual} a {nuevo_estado}: el estado solo puede avanzar")
    return repositorio.cambiar_estado(id, nuevo_estado)


def eliminar_tarea(id):
    marcadas = repositorio.eliminar_tarea(id)
    if marcadas == 0:
        raise TareaNoEncontrada(f"No existe la tarea con id {id}")


def resumen():
    return {
        "por_estado": repositorio.contar_por_estado(),
        "por_usuario": repositorio.contar_por_usuario(),
        "vencidas": repositorio.contar_vencidas()
    }
from fastapi import APIRouter, Query
from typing import Optional, Literal

from app import servicio
from app.esquemas import UsuarioCrear, TareaCrear, TareaEditar, CambioEstado

# Tres meseros, uno por grupo de rutas. El prefix evita repetir el inicio de la ruta
router_usuarios = APIRouter(prefix="/usuarios", tags=["Usuarios"])
router_tareas = APIRouter(prefix="/tareas", tags=["Tareas"])
router_reportes = APIRouter(prefix="/reportes", tags=["Reportes"])


@router_usuarios.post("", status_code=201)
def crear_usuario(datos: UsuarioCrear):
    return servicio.crear_usuario(datos.nombre, datos.email)


@router_tareas.post("", status_code=201)
def crear_tarea(datos: TareaCrear):
    return servicio.crear_tarea(datos.titulo, datos.descripcion, datos.prioridad,
                                datos.fecha_limite, datos.usuario_id)


@router_tareas.get("")
def listar_tareas(
    estado: Optional[Literal["PENDIENTE", "EN_PROGRESO", "HECHA"]] = None,
    prioridad: Optional[Literal["BAJA", "MEDIA", "ALTA"]] = None,
    usuario_id: Optional[int] = None,
    page: int = Query(default=1, ge=1),             # ge = "mayor o igual que"
    size: int = Query(default=10, ge=1, le=100),    # le = "menor o igual que"
):
    return servicio.listar_tareas(estado, prioridad, usuario_id, page, size)


@router_tareas.get("/{id}")
def obtener_tarea(id: int):
    return servicio.obtener_tarea(id)

@router_tareas.put("/{id}")
def actualizar_tarea(id: int, datos: TareaEditar):
    return servicio.actualizar_tarea(id, datos.titulo, datos.descripcion,
                                     datos.prioridad, datos.fecha_limite)

@router_tareas.patch("/{id}/estado")
def cambiar_estado(id: int, datos: CambioEstado):
    return servicio.cambiar_estado(id, datos.estado)

@router_tareas.delete("/{id}", status_code=204)
def eliminar_tarea(id: int):
    servicio.eliminar_tarea(id)


@router_reportes.get("/resumen")
def resumen():
    return servicio.resumen()
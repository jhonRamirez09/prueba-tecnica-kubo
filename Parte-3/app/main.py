from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.database import crear_tablas
from app.controlador import router_usuarios, router_tareas, router_reportes
from app.servicio import UsuarioNoEncontrado, TareaNoEncontrada, EmailDuplicado, TransicionInvalida

crear_tablas()

app = FastAPI(title="API de Gestion de Tareas")
app.include_router(router_usuarios)
app.include_router(router_tareas)
app.include_router(router_reportes)


# Todas las respuestas de error tienen el mismo formato: {"error": "...", "detalle": [...]}
def respuesta_error(codigo, mensaje, detalle=None):
    return JSONResponse(status_code=codigo, content={"error": mensaje, "detalle": detalle or []})


@app.exception_handler(UsuarioNoEncontrado)
def manejar_usuario_no_encontrado(request: Request, exc: UsuarioNoEncontrado):
    return respuesta_error(404, str(exc))

@app.exception_handler(TareaNoEncontrada)
def manejar_tarea_no_encontrada(request: Request, exc: TareaNoEncontrada):
    return respuesta_error(404, str(exc))

@app.exception_handler(EmailDuplicado)
def manejar_email_duplicado(request: Request, exc: EmailDuplicado):
    return respuesta_error(409, str(exc))

@app.exception_handler(TransicionInvalida)
def manejar_transicion_invalida(request: Request, exc: TransicionInvalida):
    return respuesta_error(409, str(exc))

# Errores de Pydantic. Si el JSON viene mal escrito -> 400; si los datos no cumplen las reglas -> 422
@app.exception_handler(RequestValidationError)
def manejar_validacion(request: Request, exc: RequestValidationError):
    errores = exc.errors()
    if any(e["type"] == "json_invalid" for e in errores):
        return respuesta_error(400, "El cuerpo de la peticion no es un JSON valido")
    detalle = [
        {"campo": ".".join(str(parte) for parte in e["loc"][1:]), "mensaje": e["msg"]}
        for e in errores
    ]
    return respuesta_error(422, "Datos de entrada invalidos", detalle)
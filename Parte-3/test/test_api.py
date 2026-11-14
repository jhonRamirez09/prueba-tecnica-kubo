from datetime import date, timedelta

MANANA = str(date.today() + timedelta(days=1))
AYER = str(date.today() - timedelta(days=1))


def crear_tarea(cliente, usuario_id, titulo="Estudiar SQL", prioridad="ALTA"):
    return cliente.post("/tareas", json={
        "titulo": titulo,
        "descripcion": "Repasar JOIN y HAVING",
        "prioridad": prioridad,
        "fecha_limite": MANANA,
        "usuario_id": usuario_id,
    })


# ------------------------------ Casos felices ------------------------------

def test_crear_tarea_devuelve_201_y_estado_pendiente(cliente, usuario):
    respuesta = crear_tarea(cliente, usuario["id"])
    assert respuesta.status_code == 201
    assert respuesta.json()["estado"] == "PENDIENTE"


def test_listar_con_filtros_y_paginacion(cliente, usuario):
    crear_tarea(cliente, usuario["id"], titulo="Tarea alta", prioridad="ALTA")
    crear_tarea(cliente, usuario["id"], titulo="Tarea baja", prioridad="BAJA")
    crear_tarea(cliente, usuario["id"], titulo="Otra alta", prioridad="ALTA")

    respuesta = cliente.get("/tareas?prioridad=ALTA&page=1&size=1")
    cuerpo = respuesta.json()
    assert respuesta.status_code == 200
    assert cuerpo["total"] == 2          # hay 2 tareas ALTA en total...
    assert len(cuerpo["items"]) == 1     # ...pero la pagina solo trae 1


def test_estado_avanza_en_orden(cliente, usuario):
    tarea = crear_tarea(cliente, usuario["id"]).json()
    r1 = cliente.patch(f"/tareas/{tarea['id']}/estado", json={"estado": "EN_PROGRESO"})
    r2 = cliente.patch(f"/tareas/{tarea['id']}/estado", json={"estado": "HECHA"})
    assert r1.json()["estado"] == "EN_PROGRESO"
    assert r2.json()["estado"] == "HECHA"


def test_borrado_logico_oculta_la_tarea(cliente, usuario):
    tarea = crear_tarea(cliente, usuario["id"]).json()
    assert cliente.delete(f"/tareas/{tarea['id']}").status_code == 204
    assert cliente.get(f"/tareas/{tarea['id']}").status_code == 404
    assert cliente.get("/tareas").json()["total"] == 0


def test_reporte_cuenta_por_estado_y_usuario(cliente, usuario):
    crear_tarea(cliente, usuario["id"])
    crear_tarea(cliente, usuario["id"])
    reporte = cliente.get("/reportes/resumen").json()
    assert reporte["por_estado"] == [{"estado": "PENDIENTE", "cantidad": 2}]
    assert reporte["por_usuario"] == [{"usuario_id": usuario["id"], "cantidad": 2}]
    assert reporte["vencidas"] == 0


# ------------------------------ Casos de error -----------------------------

def test_estado_no_puede_retroceder(cliente, usuario):
    tarea = crear_tarea(cliente, usuario["id"]).json()
    cliente.patch(f"/tareas/{tarea['id']}/estado", json={"estado": "EN_PROGRESO"})

    respuesta = cliente.patch(f"/tareas/{tarea['id']}/estado", json={"estado": "PENDIENTE"})
    assert respuesta.status_code == 409
    assert cliente.get(f"/tareas/{tarea['id']}").json()["estado"] == "EN_PROGRESO"


def test_email_duplicado_devuelve_409(cliente, usuario):
    respuesta = cliente.post("/usuarios", json={"nombre": "Otra Ana", "email": "ANA@correo.com"})
    assert respuesta.status_code == 409
    assert "error" in respuesta.json()


def test_titulo_corto_devuelve_422_con_formato_uniforme(cliente, usuario):
    respuesta = crear_tarea(cliente, usuario["id"], titulo="ab")
    cuerpo = respuesta.json()
    assert respuesta.status_code == 422
    assert set(cuerpo.keys()) == {"error", "detalle"}
    assert cuerpo["detalle"][0]["campo"] == "titulo"


def test_fecha_limite_pasada_devuelve_422(cliente, usuario):
    respuesta = cliente.post("/tareas", json={
        "titulo": "Tarea vieja", "descripcion": "x", "prioridad": "MEDIA",
        "fecha_limite": AYER, "usuario_id": usuario["id"],
    })
    assert respuesta.status_code == 422


def test_prioridad_invalida_devuelve_422(cliente, usuario):
    respuesta = crear_tarea(cliente, usuario["id"], prioridad="URGENTE")
    assert respuesta.status_code == 422


def test_tarea_inexistente_devuelve_404(cliente):
    respuesta = cliente.get("/tareas/999")
    assert respuesta.status_code == 404
    assert respuesta.json()["detalle"] == []


def test_usuario_inexistente_devuelve_404(cliente):
    respuesta = crear_tarea(cliente, usuario_id=999)
    assert respuesta.status_code == 404


def test_json_mal_formado_devuelve_400(cliente):
    respuesta = cliente.post("/tareas", content="{esto no es json",
                             headers={"Content-Type": "application/json"})
    assert respuesta.status_code == 400

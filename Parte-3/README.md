# Parte 3 · API REST de Gestión de Tareas

API para gestionar las tareas de un equipo, hecha con **Python + FastAPI + SQLite**.

## Estructura (por capas)

```
Parte-3/
  app/
    main.py          Arranca la API, registra las rutas y convierte errores en JSON
    controlador.py   Rutas HTTP: reciben la peticion y llaman al servicio (sin logica de negocio)
    servicio.py      Reglas de negocio: transicion de estados, duplicados, 404
    repositorio.py   Unico lugar que habla con la base de datos (SQL parametrizado)
    esquemas.py      Validaciones de entrada con Pydantic
    database.py      Conexion a SQLite y script de creacion de tablas
  test/
    conftest.py      Base de datos temporal para cada prueba
    test_api.py      13 pruebas automatizadas
  requirements.txt
  pytest.ini
```

El flujo de una petición: **controlador → servicio → repositorio → base de datos**.

## Instalación y ejecución

```bash
cd Parte-3
python -m venv venv
venv\Scripts\activate          # Windows  (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- API: `http://127.0.0.1:8000`
- Documentación interactiva (Swagger / OpenAPI): `http://127.0.0.1:8000/docs`

Las tablas se crean solas al arrancar (`crear_tablas()` en `database.py`), en el archivo `tareas.db`.

## Pruebas

```bash
pytest
```

Son 13 pruebas: 5 de casos felices y 8 de casos de error, incluida la regla de transición de estados. Cada prueba usa una base de datos temporal, así que no tocan `tareas.db`.

## Endpoints

| Método | Ruta | Descripción | Códigos |
|---|---|---|---|
| POST | `/usuarios` | Crear usuario (email único) | 201, 409, 422 |
| POST | `/tareas` | Crear tarea | 201, 404, 422 |
| GET | `/tareas` | Listar con filtros `estado`, `prioridad`, `usuario_id` y paginación `page`, `size` | 200, 422 |
| GET | `/tareas/{id}` | Detalle | 200, 404 |
| PUT | `/tareas/{id}` | Editar | 200, 404, 422 |
| PATCH | `/tareas/{id}/estado` | Cambiar estado (solo avanza) | 200, 404, 409, 422 |
| DELETE | `/tareas/{id}` | Borrado lógico | 204, 404 |
| GET | `/reportes/resumen` | Conteo por estado, por usuario y tareas vencidas | 200 |

Todos los errores tienen el mismo formato:

```json
{ "error": "Datos de entrada invalidos", "detalle": [{ "campo": "titulo", "mensaje": "..." }] }
```

## Ejemplos con curl

> En PowerShell usa `curl.exe` (porque `curl` ahí es otro comando). Cambia la fecha por una futura.

```bash
# Crear usuario
curl.exe -X POST http://127.0.0.1:8000/usuarios -H "Content-Type: application/json" -d "{\"nombre\":\"Ana\",\"email\":\"ana@correo.com\"}"

# Crear tarea
curl.exe -X POST http://127.0.0.1:8000/tareas -H "Content-Type: application/json" -d "{\"titulo\":\"Estudiar SQL\",\"descripcion\":\"JOIN y HAVING\",\"prioridad\":\"ALTA\",\"fecha_limite\":\"2027-01-15\",\"usuario_id\":1}"

# Listar con filtros y paginacion
curl.exe "http://127.0.0.1:8000/tareas?estado=PENDIENTE&prioridad=ALTA&page=1&size=10"

# Detalle
curl.exe http://127.0.0.1:8000/tareas/1

# Editar
curl.exe -X PUT http://127.0.0.1:8000/tareas/1 -H "Content-Type: application/json" -d "{\"titulo\":\"Estudiar SQL avanzado\",\"descripcion\":\"Funciones de ventana\",\"prioridad\":\"MEDIA\",\"fecha_limite\":\"2027-02-01\"}"

# Cambiar estado
curl.exe -X PATCH http://127.0.0.1:8000/tareas/1/estado -H "Content-Type: application/json" -d "{\"estado\":\"EN_PROGRESO\"}"

# Borrado logico
curl.exe -X DELETE http://127.0.0.1:8000/tareas/1

# Reporte
curl.exe http://127.0.0.1:8000/reportes/resumen
```

## Decisiones tomadas

- **SQLite con `sqlite3` y SQL escrito a mano**, sin ORM, para tener control total de las consultas. Todas usan parámetros `?`, lo que previene la inyección SQL.
- **Llaves foráneas activas** con `PRAGMA foreign_keys = ON`. SQLite las trae apagadas por defecto.
- **Borrado lógico:** la columna `eliminado` (0 activa, 1 borrada). Todas las consultas filtran `eliminado = 0`, así que una tarea borrada responde 404.
- **Transición de estados:** el estado solo puede avanzar (`PENDIENTE → EN_PROGRESO → HECHA`). Se permite saltar de PENDIENTE a HECHA porque el enunciado solo prohíbe retroceder. Repetir el mismo estado o retroceder devuelve **409**, porque choca con el estado actual del recurso.
- **400 vs 422:** 400 cuando el cuerpo no es un JSON válido; 422 cuando el JSON está bien escrito pero los datos no cumplen las reglas.
- **Email único sin importar mayúsculas:** se guarda en minúsculas, así `Ana@Correo.com` y `ana@correo.com` cuentan como duplicado (409).
- **Tarea vencida:** `fecha_limite` anterior a hoy y estado distinto de HECHA.
- **Nombres de columnas:** en la base la columna se llama `usuarios_id`; el repositorio la traduce a `usuario_id` para que la API use el nombre del enunciado.
- **Validación en dos capas:** Pydantic valida la entrada (título de 3 a 100 caracteres, prioridad, fecha no pasada) y el servicio valida las reglas de negocio.

## Mejoras pendientes

- Validar el formato del email con `EmailStr`.
- Autenticación JWT, Dockerfile y docker-compose (bonus).

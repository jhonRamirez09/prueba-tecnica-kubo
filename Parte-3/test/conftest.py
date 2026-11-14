import pytest
from fastapi.testclient import TestClient

from app import database
from app.main import app


@pytest.fixture(autouse=True)  # autouse=True -> corre antes de cada prueba sin pedirlo
def base_de_datos_de_prueba(tmp_path, monkeypatch):
    # tmp_path es una carpeta temporal que se borra sola; asi no se toca la base real
    monkeypatch.setattr(database, "DB_NAME", str(tmp_path / "prueba.db"))
    database.crear_tablas()


@pytest.fixture
def cliente():
    # Cliente de pruebas: hace peticiones HTTP a la API sin levantar el servidor
    return TestClient(app)


@pytest.fixture
def usuario(cliente):
    respuesta = cliente.post("/usuarios", json={"nombre": "Ana", "email": "ana@correo.com"})
    return respuesta.json()

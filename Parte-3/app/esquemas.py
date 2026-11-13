from pydantic import BaseModel, Field, field_validator
from typing import Literal
from datetime import date


class UsuarioCrear(BaseModel):
    nombre: str = Field(min_length=1)
    email: str = Field(min_length=1)


class TareaEditar(BaseModel):
    titulo: str = Field(min_length=3, max_length=100)
    descripcion: str
    prioridad: Literal["BAJA", "MEDIA", "ALTA"]
    fecha_limite: date

    @field_validator("fecha_limite")
    @classmethod
    def fecha_no_pasada(cls, valor):
        if valor < date.today():
            raise ValueError("la fecha no puede ser anterior a hoy")
        return valor


class TareaCrear(TareaEditar):
    usuario_id: int


class CambioEstado(BaseModel):
    estado: Literal["PENDIENTE", "EN_PROGRESO", "HECHA"]
from sqlmodel import Field, SQLModel
from datetime import date
from typing import Optional
from pydantic import BaseModel

class vEventos (SQLModel, table=True):
    idEvento: int | None = Field(default=None, primary_key=True)
    nombre: str
    cantidadParticipantes: int
    fechaInicio: date
    fechaFin: date
    estatus: str
    descripcion: str
    tipo_evento: str
    departamento: str

class eventos ( SQLModel, table=True):
    idEvento: Optional[int] | None = Field(default=None, primary_key=True)
    nombre: str
    cantidadParticipantes: Optional[int] = Field(default=1)
    fechaInicio: date
    fechaFin: date
    estatus: Optional[str] = Field(default="Pendiente")
    descripcion: str
    idtipo: int
    iddepartamento: int


class salida (BaseModel):
    estatus: bool
    evento: Optional[vEventos] = None
    mensaje: str

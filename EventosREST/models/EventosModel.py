from sqlmodel import SQLModel,Field
from datetime import date
from typing import Optional
from pydantic import BaseModel

class vEventos(SQLModel,table=True):
    idevento:int=Field(primary_key=True)
    nombre:str
    cantidadparticipantes:int
    fechainicio:date
    fechafin:date
    estatus:str
    descripcion:str
    tipo_evento:str
    departamento:str

class Eventos(SQLModel,table=True):
    idevento: Optional[int] = Field(primary_key=True)
    nombre: str
    cantidadparticipantes: int=Field(default=1)
    fechainicio: date
    fechafin: date
    estatus: Optional[str]=Field(default="Pendiente")
    descripcion: str
    idtipo: int
    iddepartamento: int
class Salida(BaseModel):
    estatus:bool
    mensaje:str
class EventoSalida(Salida):
    evento:vEventos|None=None

class EventoUpdate(SQLModel):
    nombre:Optional[str]=None
    cantidadparticipantes:Optional[int]=None
    descripcion:Optional[str]=None
    idtipo:Optional[int]=None
    iddepartamento:Optional[int]=None

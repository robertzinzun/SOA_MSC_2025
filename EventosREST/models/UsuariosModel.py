from sqlmodel import SQLModel,Field
from models.EventosModel import Salida
class vUsuarios(SQLModel,table=True):
    idUsuario:int=Field(primary_key=True)
    usuario:str
    telefono:str
    email:str
    genero:str
    password:str
    tipo:str
    estatus:bool
    dependencia:str
    rol:str
    departamento:str

class UsuarioSalida(Salida):
    usuario:vUsuarios|None=None

class UsuarioAutenticar(SQLModel):
    email:str
    password:str
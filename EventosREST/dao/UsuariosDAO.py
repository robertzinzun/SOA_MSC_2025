from sqlmodel import Session
from models.UsuariosModel import UsuarioSalida,vUsuarios
class UsuariosDAO():
    def __init__(self,session:Session):
        self.session=session

    def autenticar(self,email:str,password:str):
        salida=UsuarioSalida(estatus=False,mensaje="",usuario=None)
        print(password)
        usuario=self.session.query(vUsuarios).filter(vUsuarios.email==email , vUsuarios.password==password ,
                                                     vUsuarios.estatus==True , vUsuarios.tipo=='Interno').first()
        if usuario:
            salida.estatus=True
            salida.mensaje='Usuario autenticado'
            salida.usuario=usuario
        else:
            salida.estatus=False
            salida.mensaje="Datos invalidos."
        return salida
from fastapi import FastAPI,Request,HTTPException,status
import uvicorn

from dao.EventosDAO import EventosDAO
from dao.UsuariosDAO import UsuariosDAO
from dao.database import Conexion
from models.EventosModel import vEventos, Salida, Eventos, EventoSalida, EventoUpdate, EventosSalida
from datetime import date
from fastapi import Depends
from models.UsuariosModel import UsuarioAutenticar,UsuarioSalida
from fastapi.security import HTTPBasic,HTTPBasicCredentials

app=FastAPI()
security=HTTPBasic()
@app.on_event("startup")
def startup():
    conexion=Conexion()
    session=conexion.getSession()
    app.session=session
    print("Conectado con la BD")
@app.get("/")
async def inicio():
    return "Bienvenido a la API REST de EVENTOS"
def validarUsuario(request:Request,crendeciales:HTTPBasicCredentials=Depends(security)):
    uDAO=UsuariosDAO(request.app.session)
    return uDAO.autenticar(crendeciales.username,crendeciales.password)
@app.post("/eventos",summary="Crear evento",response_model=Salida, tags=["Eventos"])
async def crearEvento(evento:Eventos,request:Request,respuesta:UsuarioSalida=Depends(validarUsuario)):
    if respuesta.estatus==True and respuesta.usuario.rol in ["Administrativo","Docente","Mantenimiento"]:
        eDAO=EventosDAO(request.app.session)
        return eDAO.agregar(evento)
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="No autorizado")
@app.put("/eventos/{idEvento}",summary="Editar Evento",tags=["Eventos"],response_model=Salida)
async def modificarEvento(idEvento:int,eventoU:EventoUpdate,request:Request,security=Depends(security)):
    eDAO=EventosDAO(request.app.session)
    return eDAO.modificar(idEvento,eventoU)

@app.get("/eventos",response_model=list[vEventos],tags=["Eventos"],summary=" Consulta de Eventos")
async def consultarEventos(request:Request)->list[vEventos]:
    eDAO=EventosDAO(request.app.session)
    return eDAO.consultar()
@app.get("/eventos/{idEvento}", tags=["Eventos"],summary="Consultar evento por su ID",response_model=EventoSalida)
async def consultaIndividual(idEvento:int,request:Request)->EventoSalida:
    eDAO=EventosDAO(request.app.session)
    return eDAO.consultarPorId(idEvento)
@app.delete("/eventos/{idEvento}",summary="Eliminar Evento",tags=["Eventos"],response_model=Salida)
async def eliminarEvento(idEvento:int,request:Request)->Salida:
    eDAO=EventosDAO(request.app.session)
    return eDAO.eliminar(idEvento)
@app.patch('/eventos/{idEvento}/cambiarEstado/{estatus}',summary="Cambiar de estado",
           tags=["Eventos"],response_model=Salida)
def cambiarEstado(idEvento:int,estatus:str,request:Request)->Salida:
    eDAO=EventosDAO(request.app.session)
    return eDAO.cambiarEstado(idEvento,estatus)
@app.get('/eventos/fecha/{fecha}',summary="Consulta por fecha",tags=["Eventos"],
         response_model=EventosSalida)
def consultarPorFecha(fecha:date,request:Request,respuesta:UsuarioSalida=Depends(validarUsuario))->EventosSalida:
    if respuesta.estatus==True:
        eDAO=EventosDAO(request.app.session)
        return eDAO.consultarPorFecha(fecha)
    else:
      raise HTTPException(status.HTTP_401_UNAUTHORIZED,detail="No autorizado")


@app.post("/usuarios/autenticar",tags=["Usuarios"],summary="Autenticar Usuarios",response_model=UsuarioSalida)
async def autenticar(usuarioA:UsuarioAutenticar,request:Request)->UsuarioSalida:
    uDAO=UsuariosDAO(request.app.session)
    return uDAO.autenticar(usuarioA.email,usuarioA.password)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run("main:app",reload=True,port=8000,host="127.0.0.1")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

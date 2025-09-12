from fastapi import FastAPI,Request
import uvicorn

from dao.EventosDAO import EventosDAO
from dao.database import Conexion
from models.EventosModel import vEventos, Salida, Eventos, EventoSalida, EventoUpdate

app=FastAPI()

@app.on_event("startup")
def startup():
    conexion=Conexion()
    session=conexion.getSession()
    app.session=session
    print("Conectado con la BD")
@app.get("/")
async def inicio():
    return "Bienvenido a la API REST de EVENTOS"

@app.post("/eventos",summary="Crear evento",response_model=Salida)
async def crearEvento(evento:Eventos,request:Request):
    eDAO=EventosDAO(request.app.session)
    return eDAO.agregar(evento)
@app.put("/eventos/{idEvento}",summary="Editar Evento",tags=["Eventos"],response_model=Salida)
async def modificarEvento(idEvento:int,eventoU:EventoUpdate,request:Request):
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
@app.delete("/eventos")
async def eliminarEvento():
    return {"mensaje":"Eliminando un evento"}

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run("main:app",reload=True,port=8000,host="127.0.0.1")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

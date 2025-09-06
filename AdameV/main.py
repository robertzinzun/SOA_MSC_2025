from fastapi import FastAPI, Request
import uvicorn
from dao.database import conexion 
from dao.Eventosdao import EventosDAO
from models.eventosmodel import vEventos , salida,eventos
app = FastAPI()


@app.on_event("startup")
def startup_event():
    dbconexion = conexion()
    session = dbconexion.getSession()
    app.session = session
    print("conexion exitosa")




@app.get("/")
async def inicio():
    return "Bienvenido a la API REST de EVENTOS"


@app.post("/eventos", tags=["Eventos"], description="Crear un nuevo evento", response_model=salida)
async def crearEvento(evento: eventos, request: Request):
    dao = EventosDAO(request.app.session)
    resultado = dao.create_evento(evento)
    return resultado


@app.put("/eventos")
async def modificarEvento(evento: eventos, request: Request):
    dao = EventosDAO(request.app.session)
    resultado = dao.update_evento(evento.idEvento, evento)
    if resultado:
        return {"mensaje": "Evento modificado exitosamente"}
    return {"mensaje": "Error al modificar el evento"}


@app.get("/eventos" , response_model=list[vEventos], tags=["Eventos"] ,description="Consultar todos los eventos")
async def consultarEventos(request: Request):
    dao = EventosDAO(request.app.session)
    eventos = dao.get_all_eventos()
    return eventos


@app.get("/eventos/{idEvento}", response_model=salida, tags=["Eventos"], description="Consultar un evento por su ID")
async def consultaIndividual(idEvento: int, request: Request):
    dao = EventosDAO(request.app.session)
    return dao.get_evento(idEvento)


@app.delete("/eventos/{idEvento}", tags=["Eventos"], description="Eliminar un evento por su ID")
async def eliminarEvento(idEvento: int, request: Request):
    dao = EventosDAO(request.app.session)
    resultado = dao.delete_evento(idEvento)
    if resultado:
        return {"mensaje": "Evento eliminado exitosamente"}
    return {"mensaje": "Error al eliminar el evento"}
    return {"mensaje": "Eliminando un evento"}

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, port=8000, host="127.0.0.1")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

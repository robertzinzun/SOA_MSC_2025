from fastapi import FastAPI
import uvicorn

app=FastAPI()

@app.get("/")
async def inicio():
    return "Bienvenido a la API REST de EVENTOS"

@app.post("/eventos")
async def crearEvento():
    return {"mensaje":"Creando un evento"}
@app.put("/eventos")
async def modificarEvento():
    return {"mensaje":"Editando un evento"}

@app.get("/eventos")
async def consultarEventos():
    return {"mensaje":"Consultado un evento"}
@app.get("/eventos/{idEvento}")
async def consultaIndividual(idEvento:int):
    return {"mensaje":f'Consultando el evento con id:{idEvento}'}
@app.delete("/eventos")
async def eliminarEvento():
    return {"mensaje":"Eliminando un evento"}

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run("main:app",reload=True,port=8000,host="127.0.0.1")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

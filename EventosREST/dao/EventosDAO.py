from sqlmodel import Session
from models.EventosModel import vEventos, Eventos, Salida, EventoSalida, EventoUpdate


class EventosDAO:
    def __init__(self,session:Session):
        self.session=session
    def consultar(self):
        lista=self.session.query(vEventos).all()
        return lista
    def agregar(self,evento:Eventos):
        salida=Salida(estatus=False,mensaje="")
        try:
            self.session.add(evento)
            self.session.commit()
            self.session.refresh(evento)
            salida.estatus=True
            salida.mensaje="Evento creado con exito"
        except Exception as ex:
            salida.estatus=False
            salida.mensaje="Error al crear el evento, consulta el log para mas detalles"
            print(ex)
        return salida
    def consultarPorId(self,idEvento):
        evento=self.session.get(vEventos,idEvento)
        salida=EventoSalida(estatus=False,mensaje="",evento=None)
        if evento:
            salida.estatus=True
            salida.mensaje=f"listado del evento con id:{idEvento}"
            salida.evento=evento
        else:
            salida.estatus=False
            salida.mensaje=f"El evento con id:{idEvento} no existe"
        return salida
    def modificar(self,idEvento:int,eventoU:EventoUpdate):
        salida=Salida(estatus=False,mensaje="")
        eventoDB=self.session.get(Eventos,idEvento)
        if eventoDB and (eventoDB.estatus in ['Pendiente' or 'Proceso']):
            eventoData=eventoU.model_dump(exclude_unset=True)
            eventoDB.sqlmodel_update(eventoData)
            self.session.commit()
            self.session.refresh(eventoDB)
            salida.estatus=True
            salida.mensaje=f"Evento con id:{idEvento} modificado con exito."
        else:
            salida.estatus=False
            salida.mensaje=(f'El evento con id:{idEvento} no existe o ya fue '
                            f'Cancelado/Finalizado')
        return salida

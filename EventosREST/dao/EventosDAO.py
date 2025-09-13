import datetime

from sqlmodel import Session
from models.EventosModel import vEventos, Eventos, Salida, EventoSalida, EventoUpdate, EventosSalida
from datetime import date

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
    def cambiarEstado(self,idEvento:int,estatus:str):
        salida=Salida(estatus=False,mensaje="")
        evento=self.session.get(Eventos,idEvento)
        if evento:
            try:
                evento.estatus=estatus
                self.session.commit()
                self.session.refresh(evento)
                salida.estatus=True
                salida.mensaje=f"El evento cambio al estatus:{estatus}"
            except Exception as ex:
                print(ex)
                self.session.rollback()
                salida.estatus=False
                salida.mensaje='Error al cambiar de estatus del evento, revisa su estatus.'
        else:
            salida.estatus=False
            salida.mensaje=f'El evento con id:{idEvento} no existe.'
        return salida
    def eliminar(self,idEvento):#Eliminación fisica
        salida=Salida(estatus=False,mensaje="")
        evento=self.session.get(Eventos,idEvento)
        if evento and evento.estatus=='Cancelado':
            try:
                self.session.delete(evento)
                self.session.commit()
                salida.estatus=True
                salida.mensaje=f'El evento con id:{idEvento} fue eliminado con exito.'
            except Exception as ex:
                print(ex)
                self.session.rollback()
                salida.estatus=False
                salida.mensaje='Error, revisa el estatus del evento'
        else:
            salida.estatus=False
            salida.mensaje=f"El evento con id{idEvento} no existe o no fue cancelado."
        return salida
    def consultarPorFecha(self,fecha:date):
        salida=EventosSalida(estatus=False,mensaje="No hay eventos para esa fecha",eventos=None)
        lista=self.session.query(vEventos).filter(vEventos.fechainicio==fecha).all()
        if len(lista) > 0:
            salida.estatus=True
            salida.mensaje=f'Listado de eventos de la fecha:{fecha}'
            salida.eventos=lista
        return salida




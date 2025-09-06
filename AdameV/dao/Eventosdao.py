from sqlmodel import Session
from models.eventosmodel import vEventos, salida
class EventosDAO:
    def __init__(self, session: Session):
        self.session = session

    def create_evento(self, evento: vEventos):
        respuesta = salida(estatus=True, mensaje="Evento creado exitosamente")
        try:
            self.session.add(evento)
            self.session.commit()
            self.session.refresh(evento)
        except Exception as e:
            self.session.rollback()
            respuesta = salida(estatus=False, mensaje=str(e))
        return respuesta

    def get_evento(self, idEvento):
        evento = self.session.get(vEventos, idEvento)
        if evento:
            return salida(estatus=True, evento=evento, mensaje="Evento encontrado")
        else:
            return salida(estatus=False, evento=None, mensaje=f"Evento con id:{idEvento} no encontrado")



    def get_all_eventos(self):
        lista = self.session.query(vEventos).all()
        return lista

    def update_evento(self, idEvento, updated_evento):
        with Session(self.engine) as session:
            evento = session.get(vEventos, idEvento)
            if not evento:
                return None
            for key, value in updated_evento.dict(exclude_unset=True).items():
                setattr(evento, key, value)
            session.add(evento)
            session.commit()
            session.refresh(evento)
            return evento

    def delete_evento(self, idEvento):
        with Session(self.engine) as session:
            evento = session.get(vEventos, idEvento)
            if not evento:
                return False
            session.delete(evento)
            session.commit()
            return True
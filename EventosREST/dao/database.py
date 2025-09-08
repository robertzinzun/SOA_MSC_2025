from sqlmodel import create_engine,Session
DATABASE_URL='mysql+pymysql://staffitesz:Hola.123@localhost/GeventoSOA'
engine=create_engine(DATABASE_URL)

class Conexion:
    session=None
    def getSession(self):
        self.session=Session(engine)
        return self.session
    def cerrarSession(self):
        self.session.close()
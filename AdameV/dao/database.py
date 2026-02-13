from sqlmodel import create_engine,Session
Database_URL = "mysql+pymysql://root:root@localhost/GeventoSOA"
engine = create_engine(Database_URL)

class conexion:
    def __init__(self):
        self.session = None

    def Conectar(self):
        self.session = Session(engine)
        return self.session

    def Desconectar(self):
        if self.session:
            self.session.close()
            self.session = None
        return True

    def getSession(self):
        if self.session is None:
            self.session = Session(engine)
        return self.session
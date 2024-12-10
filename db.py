from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#El engine permite a SQLAlchemy comunicarse con la base de datos
engine = create_engine("sqlite:///database/users.db",
                       connect_args={"check_same_thread": False})
#Crear el engien no conecta inmediatamente a la base de datos

#Ahora crearemos la sesion, lo que nos permite realizar transacciones dentro de la base de datos
Session = sessionmaker(bind=engine) #Este metodo me está creando una clase de la cual yo tengo que utilizar para poder crear un objeto.
session = Session()

# Esta clase se encarga de mapear la info de las clases en las que hereda
# Y vincular su informacion a tablas de la base de datos
Base = declarative_base()
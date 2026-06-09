from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Estructura: mysql+pymysql://USUARIO:CONTRASEÑA@localhost:PUERTO/NOMBRE_BD
# REEMPLAZA 'root' y 'tu_contraseña' con los datos reales de tu MySQL
USUARIO = "root"
CONTRASENA = "28062002"  # <-- Pon aquí tu contraseña de MySQL
HOST = "localhost"
PUERTO = "3306"               # Puerto por defecto de MySQL
BD_NAME = "gallera_northwind"

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{USUARIO}:{CONTRASENA}@{HOST}:{PUERTO}/{BD_NAME}"

# Creamos el motor de conexión para MySQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Función para obtener la sesión en cada endpoint de la API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
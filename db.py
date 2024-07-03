from config import settings
from sqlalchemy import create_engine
from models.tables import Base


ur_s = settings.POSTGRES_DATABASE_URLS
ur_a = settings.POSTGRES_DATABASE_URLA

print(ur_s)

engine = create_engine(ur_s)

def create_tables():
    Base.metadata.create_all(bind=engine)
    # Base.metadata.drop_all(bind=engine)

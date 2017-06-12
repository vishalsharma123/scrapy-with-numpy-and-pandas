from sqlalchemy.engine.url import URL
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float ,String, DateTime,JSON
from sqlalchemy.orm import sessionmaker
import configparser
from directional_bottomhole import settings


DeclarativeBase = declarative_base()
DeclarativeBaseLog = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    config = configparser.ConfigParser()
    config.read('DataBase.ini')
    return create_engine(config.get('DB','sqlalchemy.url'))


def create_directional_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


class Directional_Bottomhole(DeclarativeBase):
    """Sqlalchemy Directional model"""
    __tablename__ = "directional_bottomhole_location"

    id = Column(Integer, primary_key=True)

    api_10 = Column(String(10), nullable=True)
    api_full = Column(String(15), nullable=True)
    operator = Column(String(50), nullable=True)
    well_name = Column(String(60), nullable=True)
    max_md = Column(Integer, nullable=True)
    max_tvd = Column(Integer, nullable=True)
    deviation = Column(String(55), nullable=True)
    field_code = Column(Integer, nullable=True)
    field_name = Column(String(35), nullable=True)
    checksum = Column(String(70), nullable=True)
    geom = Column(JSON, nullable=True)
    created_at = Column('created_at', DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column('updated_at', DateTime(timezone=True), onupdate=func.now(), nullable=True)


class Setup_Session(object):
    engine = db_connect()
    create_directional_table(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    try:


        session.commit()
    except:
        session.rollback()
        raise BaseException("Session Having Some issue")

    finally:
        session.close()






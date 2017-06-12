from sqlalchemy.engine.url import URL
from sqlalchemy.sql import func
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float ,String, DateTime,JSON
from sqlalchemy.orm import sessionmaker
import configparser


tankDeclarativeBase = declarative_base()



def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    config = configparser.ConfigParser()
    config.read('DataBase.ini')
    return create_engine(config.get('DB','sqlalchemy.url'))


def create_tankbatteries_table(engine):
    """"""
    tankDeclarativeBase.metadata.create_all(engine)


class tankbatteries(tankDeclarativeBase):
    """Sqlalchemy Directional model"""
    __tablename__ = "tank_batteries"

    id = Column(Integer, primary_key=True)

    fac_id = Column(String(100), nullable=True)
    fac_status = Column(String(100), nullable=True)
    fac_name = Column(String(100), nullable=True)
    fac_num = Column(String(100), nullable=True)
    loc_id = Column(String(100), nullable=True)
    oper_name= Column(String(100), nullable=True)
    oper_num = Column(String(100), nullable=True)

    utm_x = Column(String(700), nullable=True)
    utm_y = Column(String(700), nullable=True)
    county = Column(String(700), nullable=True)
    county_API = Column(String(370), nullable=True)
    wkt = Column('wkt', JSON, nullable=True)
    checksum = Column(String(270), nullable=True)
    created_at = Column('created_at', DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column('updated_at', DateTime(timezone=True), onupdate=func.now(), nullable=True)


class Setup_Session1(object):
    engine = db_connect()
    create_tankbatteries_table(engine)

    Session1 = sessionmaker(bind=engine)
    session = Session1()

    try:


        session.commit()
    except:
        session.rollback()
        raise BaseException("Session Having Some issue")

    finally:
        session.close()



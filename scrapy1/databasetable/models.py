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

def create_systemlog_table(engine):
    """"""
    DeclarativeBase.metadata.create_all(engine)


def create_production_log_table(engine):
    """ """
    DeclarativeBaseLog.metadata.create_all(engine)


class SystemLog(DeclarativeBase):
    """Log"""
    __tablename__ = "system_log"
    id = Column(Integer, primary_key=True)
    no_records = Column('no_records', Integer, nullable=True)
    scrape_type = Column('scrape_type', String(250), nullable=True)
    created_at = Column('created_at', DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column('updated_at', DateTime(timezone=True), onupdate=func.now(), nullable=True)


class ScrapyLogItem(DeclarativeBaseLog):
    """Scrapy Log"""
    __tablename__ = "scrapy_log"
    id = Column(Integer, primary_key=True)
    file_path = Column('file_path', String(250), nullable=True)
    checksum = Column('checksum', String(250), nullable=True)
    scrape_type = Column('scrape_type', String(250), nullable=True)
    created_at = Column('created_at', DateTime(timezone=True), server_default=func.now(), nullable=True)
    updated_at = Column('updated_at', DateTime(timezone=True), onupdate=func.now(), nullable=True)




class Setup_Session(object):
    engine = db_connect()
    create_production_log_table(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    try:

        session.commit()
    except:
        session.rollback()
        raise BaseException("Session Having Some issue")

    finally:
        session.close()

class Setup_Session1(object):
    engine = db_connect()
    create_systemlog_table(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    try:

        session.commit()
    except:
        session.rollback()
        raise BaseException("Session Having Some issue")

    finally:
        session.close()
class GeoInformation(DeclarativeBase):
    __tablename__ = 'geo_log'

    id = Column(Integer, primary_key=True)
    srid = Column(Integer, nullable=True)
    spider_type = Column(String(100), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    updated_at = Column(DateTime,onupdate=func.now(), nullable=True)

    def __init__(self, srid=None, spider_type=None):
        self.srid = srid
        self.spider_type = spider_type

    def __repr__(self):
        return "<GeoInformation: id='%d', srid='%d', spider_type='%s', created_at='%s', updated_at='%s'>" % (self.id, self.srid, self.spider_type, self.created_at, self.updated_at)

def create_geoInfo_table(engine):
    DeclarativeBase.metadata.create_all(engine)
class geoInfo_Session(object):
    engine = db_connect()
    create_geoInfo_table(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:

        session.commit()
    except:
        session.rollback()
        raise BaseException("Table Does Not Exist")

    finally:
        session.close()

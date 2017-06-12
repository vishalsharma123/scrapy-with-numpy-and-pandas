# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from __future__ import print_function


from directional_bottomhole.models import *

from sqlalchemy.orm import sessionmaker

from directional_bottomhole.tank_batteries_models import create_tankbatteries_table
from directional_bottomhole.utility.direction_functions import *

from directional_bottomhole.directionalmodels import create_directional_table, Directional_Bottomhole
# from directional_bottomhole.models import Data_Table, db_connect, create_deals_table

from directional_bottomhole.models import ScrapyLogItem,SystemLog
import sqlalchemy.exc
from directional_bottomhole.utility.functions import read_shapefile,get_all_checksums_from_db

from directional_bottomhole.settings import *
import os
import logging

from directional_bottomhole.utility.tankbatteries_functions import TankbatteriesAction

logger = logging.getLogger(__name__)



class DirectionalBottomholePipeline(object):

    def __init__(self):
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)
        """Creating Directional table if not exists"""
        create_directional_table(engine)


    def process_item(self, item, spider):

        directionalbottomhole = DirectionalbottomholeActions(item,self.Session)
        directionalbottomhole.insert_log(item)


class TankbatteriesPipeline(object):

    def __init__(self):
        engine = db_connect()
        self.Session = sessionmaker(bind=engine)
        """Creating Directional table if not exists"""
        create_tankbatteries_table(engine)


    def process_item(self, item, spider):

        tankbatteries = TankbatteriesAction(item,self.Session)
        tankbatteries.insert_log(item)
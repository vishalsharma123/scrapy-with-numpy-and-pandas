
from sqlalchemy import update
from directional_bottomhole import settings
from directional_bottomhole.settings import *
import directional_bottomhole
from directional_bottomhole import settings
from directional_bottomhole.directionalmodels import Directional_Bottomhole
from directional_bottomhole.models import Setup_Session, ScrapyLogItem, SystemLog, GeoInformation
from directional_bottomhole.settings import*
import hashlib
import logging
import os
import collections
import shapefile
from epsg_ident import EpsgIdent
import sqlalchemy.exc

from directional_bottomhole.tank_batteries_models import tankbatteries
from directional_bottomhole.utility.functions import read_shapefile, get_all_checksums_from_db, \
    compare_checksum_with_existing, type_cast_field

logger = logging.getLogger('systemlog')




class DirectionalbottomholeActions():


    def __init__(self, items, session):
        self.items = items
        self.Session = session
        self.previous_checksum = None
        self.previous_count = 0
        self.checksumvalues = []
        self.file_path = None
        self.directional_shape_filepath = FILES_STORE + "/Directional_Bottomhole_Locations.shp"
        self.directional_dbf_filepath = FILES_STORE + "/Directional_Bottomhole_Locations.dbf"
        self.directional_prj_filepath = FILES_STORE + "/Directional_Bottomhole_Locations.prj"

    def create_checksum(data_array):

        checksumval = ''.join(str(e) for e in data_array)

        return hashlib.sha256(str(checksumval).encode('utf-8')).hexdigest()

    def ingest_wkt(self):
        """Insert WKT from prj file, next time check if its same or not"""

        # Parse .prj file and get the SRID
        ident = EpsgIdent()
        ident.read_prj_from_file(self.directional_prj_filepath)
        srid = ident.get_epsg()
        print (srid)
        if not self.check_wkt(srid):
            logger.info("SRID is not matching")
            os._exit(1)
        try:
            if self.previous_count == 0:
                session = self.Session()
                geoLog = ({"srid": srid, "spider_type": "directional_bottomhole"})
                geoLogMask = GeoInformation(**geoLog)
                session.add(geoLogMask)
                session.commit()
            else:
                session = self.Session()
                srid_update = update(GeoInformation)
                srid_update = srid_update.where(GeoInformation.srid == srid)
                session.execute(srid_update)
                session.commit()

        except (Exception, sqlalchemy.exc.IntegrityError) as exc:
            logger.error('Database Error: %s', exc)
            session.rollback()
            raise


    def check_wkt(self, srid):

        try:
            session = self.Session()
            self.previous_count = session.query(GeoInformation.srid).filter(
                GeoInformation.spider_type == "directional_bottomhole").filter(GeoInformation.srid == srid).count()
            total_srid = session.query(GeoInformation.srid).filter(
                GeoInformation.spider_type == "directional_bottomhole").count()
            if total_srid == self.previous_count:
                return True
            else:
                return False;

        except:
            pass

    def insert_log(self, item):
        session = self.Session()
        logItems = ({"file_path": item['files'][0]['path'], "checksum":
            item['files'][0]['checksum'], "scrape_type": "directional_bottomhole"})
        """Mask log"""
        logFiles = ScrapyLogItem(**logItems)
        try:
            """Insert log into DB"""
            session.add(logFiles)
            session.commit()
            """Get the file path after extraction"""
            self.file_path = item['files'][0]['path']
            """Extract the file"""
            read_shapefile(FILES_STORE + "/" + self.file_path, FILES_STORE)
        except (Exception, sqlalchemy.exc.IntegrityError) as exc:
            logger.error('Database Error: %s', exc)
            session.rollback()
            raise
        self.directionalbottomhole_data = self.read_shape_file()
        # print(self.directionalbottomhole_data)
        self.ingest_wkt()
        self.ingest_directionalbottomhole()
    #
    def ingest_directionalbottomhole(self):
        """Merging latest COGIS Directional data into DB"""
        try:
            """Insert filtered data into the DB"""
            session = self.Session()
            session.bulk_insert_mappings(Directional_Bottomhole, self.directionalbottomhole_data)
            session.commit()
            self.inget_count_log()

        except (Exception, sqlalchemy.exc.IntegrityError) as exc:
            logger.error('Database Error: %s', exc)
            session.rollback()
        finally:
            session.close()
    #
    def inget_count_log(self):
        """Inserting the logs ( number of records )"""
        try:
            session = self.Session()
            item_inserted = (
                {"no_records": len(self.directionalbottomhole_data), "scrape_type": 'directional_bottomhole'})
            item_inserted_log = SystemLog(**item_inserted)
            session.add(item_inserted_log)
            session.commit()
        except (Exception, sqlalchemy.exc.IntegrityError) as exc:
            logger.error('Database Error: %s', exc)

            session.rollback()
        finally:
            session.close()
    #
    def read_shape_file(self):
        """Reading shape file and return the records."""
        self.checksumvalues = get_all_checksums_from_db(
            Directional_Bottomhole.checksum, self.Session())
        data = []
        # Reading shape file
        shpfile_pointer = open(self.directional_shape_filepath, "rb")
        dbffile_pointer = open(self.directional_dbf_filepath, "rb")
        sf = shapefile.Reader(shp=shpfile_pointer, dbf=dbffile_pointer)
        k = 0;
        for geomet in sf.shapeRecords():
            point_data = []  # will store geometry points
            # Create JSON object for the lat and lng
            for i, points in enumerate(geomet.shape.points):
                point_data.append({'lat': points[0]})
                point_data.append({'lng': points[1]})
            # Collect all records
            data_row = collections.OrderedDict()
            for x, shprecord in enumerate(geomet.record):
                data_row[directional_bottom_data_array[x]] = type_cast_field(shprecord) if type_cast_field(
                    shprecord) != "" else None
            checksum = hashlib.sha256(str(data_row).encode('utf-8')).hexdigest()
            data_row['checksum'] = checksum

            data_row['geom'] = geomet.shape.__geo_interface__

            if compare_checksum_with_existing(self.checksumvalues, checksum):
                # Append data_row to the parent data list
                if check_duplicate(data_row['checksum'], data):
                   data.append(data_row)
                # print(data)
        return data

def check_duplicate(checksum,data_array):


    for data_single in data_array:
        if data_single['checksum'] == checksum:
            return False

    return True
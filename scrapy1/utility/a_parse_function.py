
from sqlalchemy import update


from directional_bottomhole.models import Setup_Session1, ScrapyLogItem, SystemLog,GeoInformation
from directional_bottomhole.settings import FILES_STORE,tank_batteries_data_array
import hashlib
import logging
import os
import collections
import shapefile
from epsg_ident import EpsgIdent
import sqlalchemy.exc
from directional_bottomhole.utility.functions import read_shapefile, get_all_checksums_from_db, \
    compare_checksum_with_existing, type_cast_field
from directional_bottomhole.tank_batteries_models import tankbatteries

logger = logging.getLogger('systemlog')




class TankbatteriesAction():


    def __init__(self, items, session):
        self.items = items
        self.Session = session
        self.previous_checksum = None
        self.previous_count = 0
        self.checksumvalues = []
        self.file_path = None
        self.tankbatteries_shape_filepath = FILES_STORE + "/Tank_Batteries.shp"
        self.tankbatteries_dbf_filepath = FILES_STORE + "/Tank_Batteries.dbf"
        self.tankbatteries_prj_filepath = FILES_STORE + "/Tank_Batteries.prj"

    def create_checksum(data_array):

        checksumval = ''.join(str(e) for e in data_array)

        return hashlib.sha256(str(checksumval).encode('utf-8')).hexdigest()

    def ingest_wkt(self):
        """Insert WKT from prj file, next time check if its same or not"""

        # Parse .prj file and get the SRID
        ident = EpsgIdent()
        ident.read_prj_from_file(self.tankbatteries_prj_filepath)
        srid = ident.get_epsg()
        print (srid)
        if not self.check_wkt(srid):
            logger.info("SRID is not matching")
            os._exit(1)
        try:
            if self.previous_count == 0:
                session = self.Session()
                geoLog = ({"srid": srid, "spider_type": "tank_batteries"})
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
                GeoInformation.spider_type == "tank_batteries").filter(GeoInformation.srid == srid).count()
            total_srid = session.query(GeoInformation.srid).filter(
                GeoInformation.spider_type == "tank_batteries").count()
            if total_srid == self.previous_count:
                return True
            else:
                return False;

        except:
            pass

    def insert_log(self, item):
        session = self.Session()
        logItems = ({"file_path": item['files'][0]['path'], "checksum":
            item['files'][0]['checksum'], "scrape_type": "tank_batteries"})
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
        self.tankbatteries_data = self.read_shape_file()
        # print(self.tankbatteries_data)
        self.ingest_wkt()
        self.ingest_tankbatteries()
    #
    def ingest_tankbatteries(self):
        """Merging latest COGIS Directional data into DB"""
        try:
            """Insert filtered data into the DB"""
            session = self.Session()
            session.bulk_insert_mappings(tankbatteries, self.tankbatteries_data)
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
                {"no_records": len(self.tankbatteries_data), "scrape_type": 'tank_batteries'})
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
            tankbatteries.checksum, self.Session())
        data = []
        # Reading shape file
        shpfile_pointer = open(self.tankbatteries_shape_filepath, "rb")
        dbffile_pointer = open(self.tankbatteries_dbf_filepath, "rb")
        sf = shapefile.Reader(shp=shpfile_pointer, dbf=dbffile_pointer)
        rr = sf.shapeRecords()
        fields1 = sf.fields
        data = []
        fields = [0, 1, 2, 3, 4, 5, 6,9, 10, 16,17]
        for row, rec in enumerate(sf.shapeRecords()):
            data_row = collections.OrderedDict()
            point_data = []  # will store geometry points
            # Create JSON object for the lat and lng


            for i, j in enumerate(fields):
                data_row[tank_batteries_data_array[i]] = type_cast_field(rec.record[j]).strip() if type_cast_field(
                    rec.record[j]).strip() != "" else None
            checksum = hashlib.sha256(str(data_row).encode('utf-8')).hexdigest()

            data_row['checksum'] = checksum

            data_row['wkt'] = rec.shape.__geo_interface__
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

import hashlib
from directional_bottomhole.spiders.basic import *

import logging

from directional_bottomhole.spiders import basic


from directional_bottomhole import settings
from directional_bottomhole.settings import*

from directional_bottomhole.spiders.basic import *
import zipfile

import os
import glob
from directional_bottomhole.spiders import basic














def create_checksum(data_array):



    checksumval = ''.join(str(e) for e in data_array)

    return hashlib.sha256(str(checksumval).encode('utf-8')).hexdigest()

def compare_checksum_with_previous_date(previous_checksum,new_checksum):
    if previous_checksum == new_checksum:
        logger.info("Checksum matching with previous date")
        os._exit(1)

def get_all_checksums_from_db(table_name,session):
    checksumvalues = []
    checksumvalues = session.query(table_name)
    checksumvalues = [r for (r, ) in checksumvalues.all()]
    return checksumvalues

def compare_checksum_with_existing(checksum_list, shp_checksum):

    if shp_checksum not in checksum_list:
        return True
    else:
        return False

def type_cast_field(v):

    if isinstance(v, bytes):

        return v.decode('utf-8', errors='ignore')
    elif isinstance(v, str):

        return v
    else:
        return str(v)

def read_shapefile(filename,existing_checksum):
    for filename1 in glob.glob(os.path.join(path_to_zip_file, '*.ZIP')):
        zip_ref = zipfile.ZipFile(filename1, 'r')
        zip_ref.extractall(directory_to_extract_to)



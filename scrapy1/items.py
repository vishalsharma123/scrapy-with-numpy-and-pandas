# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html




import scrapy
from scrapy.item import  Item,Field
#

class Directional_BottomholeFilesItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()

class directionalLogItem(scrapy.Item):
    checksum = scrapy.Field()
    file_path = scrapy.Field()


class directional_bottomholeFileItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
#
class directional_bottomholeLogItem(scrapy.Item):
    checksum = scrapy.Field()
    file_path = scrapy.Field()



class directional_bottomholeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # Primary fields
    #
    file_urls = scrapy.Field()
    files = scrapy.Field()

    api_10 = scrapy.Field()
    api_full = scrapy.Field()
    Operator = scrapy.Field()
    well_name = scrapy.Field()
    bh_status = scrapy.Field()
    max_md = scrapy.Field()
    max_tvd = scrapy.Field()
    deviation = scrapy.Field()
    field_code = scrapy.Field()
    field_name = scrapy.Field()
    lattitude = scrapy.Field()
    longitude = scrapy.Field()
    utm_X = scrapy.Field()
    utm_Y = scrapy.Field()
    checksum = scrapy.Field()


class tankbatteriesFilesItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()


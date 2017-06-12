from directional_bottomhole.items import *
from directional_bottomhole.pipelines import *
from directional_bottomhole.settings import *
from directional_bottomhole.items import directional_bottomholeItem






logger = logging.getLogger(__name__)


class BasicSpider1(scrapy.Spider):
        name = "directional_bottomhole"
        allowed_domains = ["web"]
        start_urls = [direction_bottomline_url]
        custom_settings = {'ITEM_PIPELINES': {

            'directional_bottomhole.pipelines.DirectionalBottomholePipeline': 300,

            'scrapy.pipelines.files.FilesPipeline': 1

        }
        }

        def parse(self, response):
           items = Directional_BottomholeFilesItem()
           items["file_urls"] = [direction_bottomline_url]
           yield items


class BasicSpider(scrapy.Spider):
    name = "TankBattries"
    allowed_domains = ["web"]
    start_urls = [tank_batteries_url]
    custom_settings = {'ITEM_PIPELINES': {

        'directional_bottomhole.pipelines.TankbatteriesPipeline': 300,

        'scrapy.pipelines.files.FilesPipeline': 1

    }
    }

    def parse(self, response):
        items = tankbatteriesFilesItem()
        items["file_urls"] = [tank_batteries_url]
        yield items
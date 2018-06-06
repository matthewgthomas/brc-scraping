# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

from scrapy.pipelines.files import FilesPipeline
from . import spiders

class RcscraperPipeline(object):
    def process_item(self, item, spider):
        return item


class BrcFilesPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        if isinstance(info.spider, spiders.immigration.Immigration):
            return self.file_path_immigration(request, response, info)

        elif isinstance(info.spider, spiders.nhs_uk.NhsUkSpider):
            return self.file_path_nhsuk(request, response, info)

    def file_path_nhsuk(self, request, response=None, info=None):
        return os.path.join("nhs", request.url.split("/")[-1])

    def file_path_immigration(self, request, response=None, info=None):
        return os.path.join("immigration", request.url.split("/")[-1])


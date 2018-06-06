# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.files import FilesPipeline


class RcscraperPipeline(object):
    def process_item(self, item, spider):
        return item


class BrcFilesPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        return request.url.split("/")[-1]


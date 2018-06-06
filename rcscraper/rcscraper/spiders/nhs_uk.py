# -*- coding: utf-8 -*-
import scrapy


class NhsUkSpider(scrapy.Spider):
    name = 'nhs_uk'
    allowed_domains = ['https://www.england.nhs.uk/statistics/statistical-work-areas/delayed-transfers-of-care/delayed-transfers-of-care-data-2017-18/']
    start_urls = ['http://https://www.england.nhs.uk/statistics/statistical-work-areas/delayed-transfers-of-care/delayed-transfers-of-care-data-2017-18//']

    def parse(self, response):
        pass

# -*- coding: utf-8 -*-
import scrapy


class NhsUkSpider(scrapy.Spider):
    name = 'nhs_uk'
    start_urls = ['https://www.england.nhs.uk/statistics/statistical-work-areas/delayed-transfers-of-care/']

    def __init(self):
        self.year_map ={}

    def parse(self, response):
        # hxs = HtmlXPathSelector(response)  # The XPath selector
        top_level_dirs = response.xpath("//li/a[contains(text(), 'Delayed Transfers of Care')]/@href").re("(.+delayed-transfers-of-care-data-\d+)")
        for dir_url in top_level_dirs:
            yield scrapy.Request(dir_url, callback=self.parse_year_page)

    def parse_year_page(self, response):
        sites = response.xpath('//article//p/a/@href')
        return {"file_urls": [site.extract() for site in sites if site.extract()[-1] != "/"]}

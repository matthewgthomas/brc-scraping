# -*- coding: utf-8 -*-
import scrapy


class NhsUkSpider(scrapy.Spider):
    name = 'nhs_uk'
    start_urls = ['https://www.england.nhs.uk/statistics/statistical-work-areas/delayed-transfers-of-care/']

    def __init__(self):
        super(scrapy.Spider, self).__init__()
        self.year_map ={}

    def parse(self, response):
        # hxs = HtmlXPathSelector(response)  # The XPath selector
        top_level_dirs = response.xpath("//li/a[contains(text(), 'Delayed Transfers of Care')]/@href").re("(.+delayed-transfers-of-care.*\d+)")
        for dir_url in top_level_dirs:
            yield scrapy.Request(dir_url, callback=self.parse_year_page, meta={"dir": dir_url})

    def parse_year_page(self, response):
        sites_xpath = response.xpath('//article//p/a/@href')
        sites = [site.extract() for site in sites_xpath if site.extract()[-1] != "/"]

        for site in sites:
            self.year_map[site] = response.meta["dir"].split('-')[-1]
        return {"file_urls": sites}

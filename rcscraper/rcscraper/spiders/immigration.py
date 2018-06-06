# -*- coding: utf-8 -*-
import scrapy
from urllib import parse


class Immigration(scrapy.Spider):
    name = 'immigration'
    allowed_domains = ['www.gov.uk']
    start_urls = ['https://www.gov.uk/government/collections/immigration-statistics-quarterly-release']

    def parse(self, response):
        data_page_urls = response.xpath('//h3[@id="data-tables"]/following-sibling::div[@data-module="track-click"][1]/ol/li/h3/a/@href').extract()
        for url in data_page_urls:
            yield scrapy.Request(parse.urljoin(response.url, url), callback=self.parse_data_page)


    def parse_data_page(self, response):
        documents_urls = response.xpath('//section[@class="attachment embedded"]/div[@class="attachment-details"]/h2/a/@href').extract()
        return {"file_urls": [parse.urljoin(response.url, doc_url) for doc_url in documents_urls]}

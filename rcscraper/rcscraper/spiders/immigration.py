# -*- coding: utf-8 -*-
import scrapy
from urllib import parse


class Immigration(scrapy.Spider):
    name = 'immigration'
    allowed_domains = ['www.gov.uk']
    start_urls = ['https://www.gov.uk/government/collections/immigration-statistics-quarterly-release']


    def __init__(self):
        super(scrapy.Spider, self).__init__()
        self.section_map ={}

    def parse(self, response):
        data_page_links = response.xpath('//h3[@id="data-tables"]/following-sibling::div[@data-module="track-click"][1]/ol/li/h3/a')
        for link in data_page_links:
            link_text = link.xpath('text()').extract_first()
            url = link.xpath('@href').extract_first()

            yield scrapy.Request(
                parse.urljoin(response.url, url),
                callback=self.parse_data_page,
                meta={'section': link_text}
            )


    def parse_data_page(self, response):
        document_urls = response.xpath('//section[@class="attachment embedded"]/div[@class="attachment-details"]/h2/a/@href')

        file_urls = []

        for doc_url in document_urls:
            url = doc_url.extract()
            url = parse.urljoin(response.url, url)
            self.section_map[url] = response.meta['section']
            file_urls.append(url)

        return {"file_urls": file_urls}

# -*- coding: utf-8 -*-
import scrapy
from urllib import parse


class ModernSlavery(scrapy.Spider):
    name = 'modern_slavery'
    allowed_domains = ['www.gov.uk']
    start_urls = ['https://www.gov.uk/government/collections/modern-slavery']


    def __init__(self):
        super(scrapy.Spider, self).__init__()
        self.section_map ={}


    def parse(self, response):
        research_and_pub_links = response.xpath('//h3[@id="research-and-publications"]/following-sibling::div[@data-module="track-click"][1]/ol/li/ul/li[contains(text(), "Corporate report")]/../../h3/a')
        for link in research_and_pub_links:
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

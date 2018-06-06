import os

import pdf_process

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


# process = CrawlerProcess(get_project_settings())

# 'followall' is the name of one of the spiders of the project.
process.crawl('immigration')
process.start() # the script will block here until the crawling is finished
process.crawl('nhs_uk')
process.start() # the script will block here until the crawling is finished


for root, dirs, files in os.walk("files"):
    for file in files:
        if file.endswith(".pdf"):
             print(os.path.join(root, file))
             pdf_process.process(os.path.join(root, file))

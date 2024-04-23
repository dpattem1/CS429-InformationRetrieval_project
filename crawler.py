import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class MySpider(scrapy.Spider):
    name = 'webcrawler'
    allowed_domains = ['https://www.w3.org/TR/html4/struct/links.html#h-12.2.4']
    start_urls = ['https://www.w3.org/TR/html4/struct/links.html#h-12.2.4']

    custom_settings = {
        'DEPTH_LIMIT': 3,
        'CLOSESPIDER_PAGECOUNT': 100,
        'AUTOTHROTTLE_ENABLED': True
    }

    def parse(self, response):
        yield {
            'url': response.url,
            'content': response.text
        }

if __name__ == "__main__":
    process = CrawlerProcess(settings=get_project_settings())
    process.crawl(MySpider)
    process.start()

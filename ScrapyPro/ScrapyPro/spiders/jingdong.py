# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ScrapyPro.jingdongItems import ClassItem

class JingdongSpider(CrawlSpider):
    name = 'jingdong'
    allowed_domains = ['item.jd.com']
    start_urls = ['http://item.jd.com']
    rules = [Rule(LinkExtractor(allow=['/\d+\.html']), 'parse_class')]

    def parse_class(self, response):
        item = ClassItem()
        item['url'] = response.url
        item['name'] = response.xpath("//title/text()").extract()
        return item

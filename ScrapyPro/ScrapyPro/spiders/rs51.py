# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ScrapyPro.rs51Items import Rs51Item

class RsSpider(CrawlSpider):
    name = 'rs51'
    allowed_domains = ['rs05.com']
    start_urls = ['http://www.rs05.com']
    rules = [Rule(LinkExtractor(allow=['/(www.rs05.com)$']), 'parse_rs51')]

    def parse_rs51(self, response):
        item = Rs51Item()
        item['url'] = response.xpath("//ul[@class='txt-nav']//a/@href").extract()
        item['name'] = response.xpath("//ul[@class='txt-nav']//a/text()").extract()
        return item

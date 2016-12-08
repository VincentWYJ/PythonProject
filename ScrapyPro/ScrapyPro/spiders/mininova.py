# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ScrapyPro.mininovaItems import TorrentItem

class MininovaSpider(CrawlSpider):
    name = 'mininova'
    allowed_domains = ['mininova.org']
    start_urls = ['http://www.mininova.org']
    rules = [Rule(LinkExtractor(allow=['/tor/\d+']), 'parse_torrent')]

    def parse_torrent(self, response):
        item = TorrentItem()
        item['url'] = response.url
        item['name'] = response.xpath("//h1/text()").extract()
        item['description'] = response.xpath("//div[@id='description']/text()").extract()
        item['size'] = response.xpath("//div[@id='specifications']/p[2]/text()[2]").extract()
        return item

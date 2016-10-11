# -*- coding: utf-8 -*-
import scrapy


class EchrSpider(scrapy.Spider):
    name = "echr"
    allowed_domains = ["hudoc.echr.coe.int"]
    start_urls = (
        'http://www.hudoc.echr.coe.int/',
    )

    def parse(self, response):
        pass

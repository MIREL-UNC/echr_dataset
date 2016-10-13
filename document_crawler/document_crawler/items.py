# -*- coding: utf-8 -*-
"""Items to abstract ECHR documents."""

import scrapy


class Document(scrapy.Item):
    """Abstraction of a ECHR scraped document."""
    name = scrapy.Field()
    doctype = scrapy.Field()
    sentences = scrapy.Field()
    original_id = scrapy.Field()
    language = scrapy.Field()
    conclusion = scrapy.Field()
    originatingbody = scrapy.Field()
    application = scrapy.Field()
    title = scrapy.Field()

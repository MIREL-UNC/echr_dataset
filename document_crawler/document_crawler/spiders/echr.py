# -*- coding: utf-8 -*-
"""Scraper for ECHR page."""
import json
import logging
import scrapy

from document_crawler.items import Document

DEFAULT_LIMIT = 10
RESULT_PER_PAGE = 50


class EchrSpider(scrapy.Spider):
    """Crawler for the ECHR page. Obtains all documents in English."""
    # URL to get the list of documents
    base_main_url = ('http://hudoc.echr.coe.int/app/query/results?query='
        '((((((((((((((((((((%20contentsitename%3AECHR%20AND%20(NOT%20('
        'doctype%3DPR%20OR%20doctype%3DHFCOMOLD%20OR%20doctype%3DHECOMOLD))'
        '%20AND%20((languageisocode%3D%22ENG%22))%20AND%20(('
        'documentcollectionid%3D%22GRANDCHAMBER%22)%20OR%20('
        'documentcollectionid%3D%22CHAMBER%22)))%20XRANK(cb%3D14)'
        '%20doctypebranch%3AGRANDCHAMBER)%20XRANK(cb%3D13)%20doctypebranch'
        '%3ADECGRANDCHAMBER)%20XRANK(cb%3D12)%20doctypebranch%3ACHAMBER)%20'
        'XRANK(cb%3D11)%20doctypebranch%3AADMISSIBILITY)%20XRANK(cb%3D10)%20'
        'doctypebranch%3ACOMMITTEE)%20XRANK(cb%3D9)%20doctypebranch%3A'
        'ADMISSIBILITYCOM)%20XRANK(cb%3D8)%20doctypebranch%3ADECCOMMISSION)%20'
        'XRANK(cb%3D7)%20doctypebranch%3ACOMMUNICATEDCASES)%20XRANK(cb%3D6)%20'
        'doctypebranch%3ACLIN)%20XRANK(cb%3D5)%20doctypebranch%3A'
        'ADVISORYOPINIONS)%20XRANK(cb%3D4)%20doctypebranch%3AREPORTS)%20XRANK('
        'cb%3D3)%20doctypebranch%3AEXECUTION)%20XRANK(cb%3D2)%20doctypebranch'
        '%3AMERITS)%20XRANK(cb%3D1)%20doctypebranch%3ASCREENINGPANEL)%20XRANK('
        'cb%3D4)%20importance%3A1)%20XRANK(cb%3D3)%20importance%3A2)%20XRANK('
        'cb%3D2)%20importance%3A3)%20XRANK(cb%3D1)%20importance%3A4)%20XRANK('
        'cb%3D2)%20languageisocode%3AENG)%20XRANK(cb%3D1)%20languageisocode%3A'
        'ENG&select=sharepointid,Rank,itemid,docname,doctype,application,appno,'
        'conclusion,importance,originatingbody,typedescription,kpdate,'
        'kpdateAsText,documentcollectionid,documentcollectionid2,'
        'languageisocode,extractedappno,isplaceholder,doctypebranch,respondent,'
        'respondentOrderEng,ecli&sort=&start={start_index}&length={length}'
        '&rankingModelId=4180000c-8692-45ca-ad63-74bc4163871b')
    # URL to query each documents from its id.
    base_document_url = ('http://hudoc.echr.coe.int/app/conversion/docx/html/'
        'body?library=ECHR&id={}')
    name = 'echr'
    allowed_domains = ['hudoc.echr.coe.int']
    start_urls = (
        base_main_url.format(start_index=0, length=RESULT_PER_PAGE),
    )

    @staticmethod
    def _create_document(result_dict):
        """Fills a new instance of Document from result_dict values"""
        document = Document(
            name=result_dict['docname'],
            original_id=result_dict['itemid'],
            doctype=result_dict['doctype'],
            language=result_dict['languageisocode'],
            conclusion=result_dict['conclusion'],
            originatingbody=result_dict['originatingbody'],
            application=result_dict['application'],
        )
        return document

    def parse(self, response):
        """Obtains the document ids and queries each of them."""
        json_response = json.loads(response.text)
        fetched_results = len(json_response['results'])

        if not hasattr(self, 'processed_results'):
            self.processed_results = 0
        self.processed_results += fetched_results
        if fetched_results == 0:
            logging.info('No more files. Total files queried {}'.format(
                self.processed_results))
            return

        for result in json_response['results']:
            document = self._create_document(result['columns'])
            if document['language'] != u'ENG':
                info = 'Case {} {} not in ENG, original language {}'.format(
                    document['original_id'], document['name'].encode('utf-8'),
                    result['columns']['languageisocode'])
                logging.info(info)
                continue
            doc_url = self.base_document_url.format(document['original_id'])
            new_request = scrapy.Request(doc_url, callback=self.parse_document)
            new_request.meta['document'] = document
            yield new_request

        if self.processed_results < int(getattr(self, 'limit', DEFAULT_LIMIT)):
            next_url = self.base_main_url.format(
                start_index=self.processed_results, length=RESULT_PER_PAGE)
            yield scrapy.Request(next_url, callback=self.parse)
        else:
            logging.info('Limit reached. Total files obtained {}'.format(
                self.processed_results))

    def parse_document(self, response):
        """Queries single documents and stores the result."""
        document = response.meta['document']
        document['title'] = ' '.join(response.css('p.s32B251D').css(
            'span.s7D2086B4 ::text').extract())
        paragraphs = []
        for paragraph in response.css('p'):
            spans = [span for span in paragraph.css('span ::text').extract()
                     if span != u'\xa0' and span != '']
            if len(spans):
                paragraphs.append(u' '.join(spans))
        document['sentences'] = paragraphs
        yield document

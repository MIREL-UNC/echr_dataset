# -*- coding: utf-8 -*-
import json
import scrapy


SAMPLE_URL = 'http://hudoc.echr.coe.int/app/query/results?query=((((((((((((((((((((%20contentsitename%3AECHR%20AND%20(NOT%20(doctype%3DPR%20OR%20doctype%3DHFCOMOLD%20OR%20doctype%3DHECOMOLD))%20AND%20((documentcollectionid%3D%22GRANDCHAMBER%22)%20OR%20(documentcollectionid%3D%22CHAMBER%22)))%20XRANK(cb%3D14)%20doctypebranch%3AGRANDCHAMBER)%20XRANK(cb%3D13)%20doctypebranch%3ADECGRANDCHAMBER)%20XRANK(cb%3D12)%20doctypebranch%3ACHAMBER)%20XRANK(cb%3D11)%20doctypebranch%3AADMISSIBILITY)%20XRANK(cb%3D10)%20doctypebranch%3ACOMMITTEE)%20XRANK(cb%3D9)%20doctypebranch%3AADMISSIBILITYCOM)%20XRANK(cb%3D8)%20doctypebranch%3ADECCOMMISSION)%20XRANK(cb%3D7)%20doctypebranch%3ACOMMUNICATEDCASES)%20XRANK(cb%3D6)%20doctypebranch%3ACLIN)%20XRANK(cb%3D5)%20doctypebranch%3AADVISORYOPINIONS)%20XRANK(cb%3D4)%20doctypebranch%3AREPORTS)%20XRANK(cb%3D3)%20doctypebranch%3AEXECUTION)%20XRANK(cb%3D2)%20doctypebranch%3AMERITS)%20XRANK(cb%3D1)%20doctypebranch%3ASCREENINGPANEL)%20XRANK(cb%3D4)%20importance%3A1)%20XRANK(cb%3D3)%20importance%3A2)%20XRANK(cb%3D2)%20importance%3A3)%20XRANK(cb%3D1)%20importance%3A4)%20XRANK(cb%3D2)%20languageisocode%3AENG)%20XRANK(cb%3D1)%20languageisocode%3AFRE&select=sharepointid,Rank,itemid,docname,doctype,application,appno,conclusion,importance,originatingbody,typedescription,kpdate,kpdateAsText,documentcollectionid,documentcollectionid2,languageisocode,extractedappno,isplaceholder,doctypebranch,respondent,respondentOrderEng,ecli&sort=&start=0&length=20&rankingModelId=4180000c-8692-45ca-ad63-74bc4163871b'



class EchrSpider(scrapy.Spider):
    name = "echr"
    allowed_domains = ["hudoc.echr.coe.int"]
    start_urls = (
        SAMPLE_URL,
    )
    # URL to query each documents from its id.
    base_document_url = 'http://hudoc.echr.coe.int/app/conversion/docx/html/body?library=ECHR&id={}'

    def parse(self, response):
        """Obtains the document ids and queries each of them."""
        json_response = json.loads(response.text)
        if json_response['resultcount'] == 0:
            print 'No result'
        for result in json_response['results']:
            if result['columns']['languageisocode'] != u'ENG':
                continue
            document_name = result['columns']['docname']
            document_id = result['columns']['itemid']
            print document_name, document_id

    def parse_document(self, response):
        """Queries single documents and stores the result."""
        title = response.css('p.s32B251D').css(
            'span.s7D2086B4 ::text').extract()

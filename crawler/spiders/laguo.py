# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings
from crawler.items import MovieInfoItem, ImageItem
import json


class LaguoSpider(scrapy.Spider):
    name = 'laguo'
    # allowed_domains = ['laguo.com']
    start_urls = ['https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false&isSchoolJob=0']

    form_data = {"first": "true", "pn": '1', "kd": "java"}

    def start_requests(self):
        return [
            scrapy.http.FormRequest(url=self.start_urls[0],
                                    headers=settings['LAGUO_REQUEST_HEADERS'],
                                    formdata=self.form_data,
                                    callback=self.parsess
                                    )]

    def parsess(self, response):
        results = json.loads(response.body_as_unicode())
        print(results['content'])

# -*- coding: utf-8 -*-
import scrapy
from scrapy.conf import settings
from login.items import MovieInfoItem, ImageItem


# import urlparse

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://accounts.douban.com/login', ]

    form_data = {
        'form-email': 'codefork1995@gmail.com',
        'form-password': 'cn1575zh',
        'redir': 'https://www.douban.com',
        'source': 'index_nav',
        'login': '登录',
    }

    # 重写
    def start_requests(self):
        return [
            scrapy.Request(url=self.start_urls[0],
                           headers=settings['DEFAULT_REQUEST_HEADERS'],
                           meta={'cookiejar': 1},
                           callback=self.parse_validate_image
                           )]

    def parse_validate_image(self, response):
        # 如果有验证码的话就手动输入验证码
        if 'captcha_image' in str(response.body):
            print('Copy the link:')
            link = response.xpath('//img[@id="captcha_image"]/@src').extract()[0]
            print(link)
            captcha_solution = input('captcha-solution:')
            # python2.7
            # captcha_id = urlparse.parse_qs(urlparse.urlparse(link).query, True)['id']
            captcha_id = link.split("?")[1].split(":")[0].split("=")[1]

            self.form_data['captcha-solution'] = captcha_solution
            self.form_data['captcha-id'] = captcha_id
        client_headers = settings['DEFAULT_REQUEST_HEADERS']
        client_headers['Host'] = 'accounts.douban.com'
        print(client_headers)
        return [scrapy.FormRequest.from_response(response,
                                                 formdata=self.form_data,
                                                 headers=client_headers,
                                                 meta={'cookiejar': response.meta['cookiejar']},
                                                 callback=self.parsefs
                                                 )]

    # def after_login(self, response):
    #     yield {'status': response.status}
    # self.headers['Host'] = 'https://www.douban.com'
    # yield scrapy.Request(url='',
    #                      meta={'cookiejar': response.meta['cookiejar']},
    #                      headers=self.headers,
    #                      callback=self.parse_comment_url
    #                      )
    # yield scrapy.Request(url='',
    #                      meta=
    #                      headers,
    #                      callback=self,
    #                      # 去重
    #                      dont_filter=,
    #                      )

    def parsefs(self, response):
        print(response.status)
        print(response.meta['cookiejar'])

        client_headers = settings['DEFAULT_REQUEST_HEADERS']
        client_headers['Host'] = 'movie.douban.com'
        print(client_headers)
        yield scrapy.Request(url="https://movie.douban.com/top250",
                             meta={'cookiejar': response.meta['cookiejar']},
                             headers=client_headers,
                             callback=self.parse_top,
                             )

    def parse_top(self, response):

        movieinfoItem = MovieInfoItem()
        for x in response.xpath("//div[@class='info']"):
            title = x.xpath("div[@class='hd']/a/span[1]/text()").extract()[0]
            star = x.xpath("div[@class='bd']/div[1]/span[2]/text()").extract()[0]
            movie_url = x.xpath("div[@class='hd']/a/@href").extract()[0]
            movieinfoItem['movie_name'] = title
            movieinfoItem['movie_star'] = star
            movieinfoItem['movie_url'] = movie_url
            yield movieinfoItem
        # imageItem=ImageItem()
        # item=[]
        # for x in response.xpath("//div[@class='item']"):
        #     images_urls=x.xpath("div[@class='pic']/a/img/@src").extract()[0]
        #     item.append(images_urls)
        # imageItem['image_urls']=item
        # return imageItem

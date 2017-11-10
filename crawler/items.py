# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # movie 电影
    movie_name=scrapy.Field()
    movie_star=scrapy.Field()
    movie_url=scrapy.Field()

class ImageItem(scrapy.Item):
    image_urls=scrapy.Field()
    images=scrapy.Field()
    image_path=scrapy.Field()


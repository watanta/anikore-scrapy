# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity


class AnikorescrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class UserscrapyItem(scrapy.Item):
    user_name = scrapy.Field()
    profile = scrapy.Field()
    user_id = scrapy.Field()
    birth_data = scrapy.Field()
    sex = scrapy.Field()
    birthplace = scrapy.Field()
    affiliation = scrapy.Field()
    animes_on_shelf = scrapy.Field()
    reviews_num = scrapy.Field()
    thankyou_num = scrapy.Field()
    more_profile = scrapy.Field()
    animes_fav_url = scrapy.Field()
    animes_plan_url = scrapy.Field()
    animes_watching_url = scrapy.Field()
    animes_dropped_url = scrapy.Field()
    animes_completed_url = scrapy.Field()
    animes_nocategory_url = scrapy.Field()

class ReviewscrapyItem(scrapy.Item):
    anime_id = scrapy.Field()
    timestamp = scrapy.Field()
    reviewer = scrapy.Field()
    reviewer_url = scrapy.Field()
    review_state = scrapy.Field()
    reading_num = scrapy.Field()
    point = scrapy.Field()
    point_story = scrapy.Field()
    point_animation = scrapy.Field()
    point_vc = scrapy.Field()
    point_music = scrapy.Field()
    point_chara = scrapy.Field()
    review_url = scrapy.Field()
    review_id  = scrapy.Field()
    review_text = scrapy.Field()


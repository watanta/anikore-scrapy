# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy.http import Request
import re


def nonetostr(str):
    if str is None:
        return ''
    return str

class ReviewsSpider(scrapy.Spider):
    name = 'reviews'
    allowed_domains = ['anikore.jp']
    start_urls = ['https://www.anikore.jp/anime_review/1']

    def __init__(self):
        self.anime_id = 1

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                endpoint='render.html',
                args={'wait': 0.5},
            )

    def parse(self, response):
        if self.anime_id == 12500: #id limit
            pass
        else:
            anime_id = self.anime_id
            reveiws = response.xpath('//*[@id="anime_detail_reviews"]/div/div[@class="anime_title_eval"]')
            for review in reveiws:
                timestamp = review.xpath('.//span[@class="ateval_dtreviewed"]/text()').extract()
                reviewer = review.xpath('.//span[@class="ateval_reviewer"]/a/text()').extract()
                reviewer_url = review.xpath('.//span[@class="ateval_reviewer"]/a/@href').extract()
                reading_num = review.xpath('.//span[@class="ateval_reviewer"]/span[@class="red bold"]/text()').extract()
                point = review.xpath('.//span[@class="ateval_rating"]//span/text()').extract()
                point_story = review.xpath('.//span[@class="ateval_ratings"]/span[1]/text()').extract()
                point_animation = review.xpath('.//span[@class="ateval_ratings"]/span[2]/text()').extract()
                point_vc = review.xpath('.//span[@class="ateval_ratings"]/span[3]/text()').extract()
                point_music = review.xpath('.//span[@class="ateval_ratings"]/span[4]/text()').extract()
                point_chara = review.xpath('.//span[@class="ateval_ratings"]/span[5]/text()').extract()
                #if review text exist, review_url is in it. 
                review_url1 = review.xpath('.//h3[@class="ateval_summary"]/a/@href').extract_first()
                #if reveiw text does NOT exist,review_url is in it.
                review_url2 = review.xpath('.//span[@class="ateval_rating"]//a/@href').extract_first()
                review_url1 = nonetostr(review_url1)
                review_url2 = nonetostr(review_url2)

                review_url = review_url1 + review_url2

                review_id = re.findall('[0-9]+', review_url)[0]

                review_text1 = review.xpath('.//span[@class="review_content"]/text()').extract()
                review_text2 = review.xpath('.//p[@class="ateval_description"]/text()').extract()
                review_text1 = nonetostr(review_text1)
                review_text2 = nonetostr(review_text2)
                review_text = review_text1 + review_text2



                yield {'anime_id':anime_id, 'timestamp':timestamp, 'reviewer':reviewer, 'reviewer_url':reviewer_url, 'reading_num':reading_num,\
                'point':point, 'point_story':point_story, 'point_animation':point_animation, \
                'point_vc':point_vc, 'point_music':point_music, 'point_chara':point_chara,\
                'review_url':review_url, 'review_id':review_id, 'review_text':review_text}

            self.anime_id +=1
            url = 'https://www.anikore.jp/anime_review/' + str(self.anime_id) + '/'

            yield Request(url, callback=self.parse, dont_filter=True)

    
# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class AnimeSpider(scrapy.Spider):
    name = 'anime'
    allowed_domains = ['anikore.jp']
    start_urls = ['http://www.anikore.jp/anime/1']
    
    def __init__(self):
        self.num = 1
        self.limit_id = 12500# until crawl until this id 


    def parse(self, response):
        if self.num == self.limit_id: 
            pass
        else:
            url = 'http://anikore.jp/anime/' + str(self.num) +  '/'


            anime_id = self.num
            title = response.xpath('//*[@id="clm24"]//h2/a[@class="blk_lnk"]/text()').extract_first()
            point = response.xpath('//*[@id="main"]/div[2]/div[2]/div[1]/div[1]/span[2]/text()').extract()
            point_story = response.xpath('//*[@id="main"]/div[2]/div[2]/div[1]/div[2]/span[2]/text()').extract()
            point_animation = response.xpath('//*[@id="main"]/div[2]/div[2]/div[1]/div[3]/span[2]/text()').extract()
            point_vc = response.xpath('//*[@id="main"]/div[2]/div[2]/div[1]/div[4]/span[2]/text()').extract()
            point_music = response.xpath('//*[@id="main"]/div[2]/div[2]/div[1]/div[5]/span[2]/text()').extract()
            point_chara = response.xpath('//*[@id="main"]/div[2]/div[2]/div[1]/div[6]/span[2]/text()').extract()
            total_point = response.xpath('//*[@id="main"]/div[2]/div[2]/div[2]/div[1]/span[2]/text()').extract()
            review_num = response.xpath('//*[@id="main"]/div[2]/div[2]/div[2]/div[2]/span[2]/text()').extract()
            fav_num = response.xpath('//*[@id="main"]/div[2]/div[2]/div[2]/div[3]/span[2]/text()').extract()
            ranking = response.xpath('//*[@id="main"]/div[2]/div[2]/div[2]/div[4]/span[2]/text()').extract()
            summary = response.xpath('//*[@id="main"]/div[2]/div[3]/blockquote/text()').extract()
    	    
            print("____________________________________________________")
            print(self.num)
            
            self.num += 1


            # if anime page exist
            if title is not None:


                #output 
                yield {"anime_id":anime_id,"title":title,"point":point,"point_story":point_story,"point_animation":point_animation, \
                "point_vc":point_vc,"point_music":point_music,"point_chara":point_chara, \
                "total_point":total_point, "review_num":review_num, "fav_num":fav_num, \
                "ranking":ranking, "summary":summary}

                # crawl next anime page
                next_url = 'http://anikore.jp/anime/' + str(self.num) +  '/'
                yield Request(next_url, callback=self.parse, dont_filter=True)
            # If animepage does not exist, redirect to homepage. So, title is None.
            else:

                #crawl next anime page
                next_url = 'http://anikore.jp/anime/' + str(self.num) +  '/'
                yield Request(next_url, callback=self.parse, dont_filter=True)
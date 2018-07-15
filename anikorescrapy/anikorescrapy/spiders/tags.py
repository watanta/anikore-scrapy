# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
#from anikorescrapy.items import TagsItem


class TagsSpider(scrapy.Spider):


    name = 'tagsj'
    allowed_domains = ['anikore.jp']
    #start_urls = ['https://www.anikore.jp/anime_tag/1/']
    start_urls = ['https://www.anikore.jp/anime_tag/1']


    def __init__(self):
        self.num = 1

    def parse(self, response):
            
            if self.num == 12500:
                pass
            else:
                title =  response.xpath('/html/body/div[4]/ul/li[6]/a/text()').extract_first()
                anime_url = "https://www.anikore.jp/anime_tag/" + str(self.num) +"/"
                anime_id = self.num
                tag_name = response.xpath('//*//div[@class="animeDetailContentBlockTagUnitTitle"]/a/span[1]/text()').extract()
                tag_num = response.xpath('//*//div[@class="animeDetailContentBlockTagUnitTitle"]/a/span[2]/text()').extract()


                tag_dict = {}

                i = 0

                for tag, num in zip(tag_name, tag_num):
                    i += 1
                    tag = tag.replace('.','_')
                    tag_set = {}
                    tag_set[tag] = num
                    tag_dict["tag" + str(i)] = tag_set
                    




                tag_dict["anime_id"] = anime_id
                tag_dict["title"] = title


                print("____________________________________________________")
                print(self.num)
                
                self.num += 1



                if title is not None:

                    yield tag_dict

                    next_url = 'http://anikore.jp/anime_tag/' + str(self.num) +  '/'

                    yield Request(next_url, callback=self.parse, dont_filter=True)
                # If animepage does not exist, redirect to homepage. So, title is None.
                else:

                    next_url = 'http://anikore.jp/anime_tag/' + str(self.num) +  '/'

                    yield Request(next_url, callback=self.parse, dont_filter=True)
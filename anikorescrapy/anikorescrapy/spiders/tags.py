# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re



class TagsSpider(scrapy.Spider):


	name = 'tags'
	allowed_domains = ['anikore.jp']
	#start_urls = ['https://www.anikore.jp/anime_tag/1/']
	start_urls = ['http://anikore.jp/chronicle']


	def parse(self, response):
		anime_years_urls = response.xpath('//*[@id="main"]//h3/a/@href').extract()
		for url in anime_years_urls:
			yield Request(url, callback=self.parse_anime)

	def parse_anime(self, response):
		anime_urls = response.xpath('//*[@id="main"]//span[@class="animeTitle"]/a/@href').extract()
		for url in anime_urls:
			absolute_url = response.urljoin(url)
			yield Request(absolute_url, callback=self.parse_anime_detail)
		#go to next page
		next_url = response.xpath('//*[@id="main"]//a[@class="next"]/@href').extract_first()
		absolute_url = response.urljoin(next_url)
		yield Request(absolute_url, callback=self.parse_anime)

	def parse_anime_detail(self, response):
		tag_url = response.xpath('//*[@id="main"]//div[@class="naturalFont animeDetailContentBlockMoreBtn"]/a/@href').extract()[1]
		yield Request(tag_url, callback=self.parse_anime_tags)


	def parse_anime_tags(self, response):

		title =  response.xpath('/html/body/div[4]/ul/li[6]/a/text()').extract_first()
		anime_url = response.xpath('/html/body/div[4]/ul/li[6]/a/@href').extract_first()
		anime_id = re.findall('[0-9]+', anime_url)[0]
		tag_name = response.xpath('//*//div[@class="animeDetailContentBlockTagUnitTitle"]/a/span[1]/text()').extract()
		tag_num = response.xpath('//*//div[@class="animeDetailContentBlockTagUnitTitle"]/a/span[2]/text()').extract()

		tag_dict = {}

		i = 0

		for tag, num in zip(tag_name, tag_num):
			i += 1
			tag_set = {}
			tag_set[tag] = num
			tag_dict["tag" + str(i)] = tag_set

		
		tag_dict["anime_id"] = anime_id
		tag_dict["title"] = title

		yield tag_dict

		#url = "https://www.anikore.jp/anime_tag/" + str(int(anime_id)+1) + "/"

		#if url is not exit, redirect to home page. so title is None.
		# if title == None:
		# 	pass
		# else:
		# 	yield Request(url, callback=self.parse)
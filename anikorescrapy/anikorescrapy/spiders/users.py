# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.utils.response import open_in_browser
from anikorescrapy.items import UserscrapyItem
from scrapy.loader import ItemLoader




class UsersSpider(scrapy.Spider):
    name = 'users'
    allowed_domains = ['anikore.jp']
    start_urls = ['https://www.anikore.jp/users/login/']



    def __init__(self):
        self.user_id = 106166
        self.user_url = "https://www.anikore.jp/users/profile/"+str(self.user_id)+"/"

        self.mail = "watanabe101watanabe@yahoo.co.jp"
        self.password = "watawata"


    def parse(self, response):
        #open_in_browser(response)

        print(response.meta)
        response.meta['handle_httpstatus_all'] = True
        print(response.meta)

        token_key = response.xpath('//div[@style="display:none;"]/input[@name="data[_Token][key]"]/@value').extract_first()
        token_fields = response.xpath('//div[@style="display:none;"]/input[@name="data[_Token][fields]"]/@value').extract()[1]
        formnumber = 1



        return scrapy.FormRequest.from_response(
            response,
            formnumber=formnumber,
            formdata={'data[User][email]': self.mail,'data[User][password]': self.password, 'data[User][remember_me]': '0'},
            callback=self.after_login
            )


    def after_login(self, response):
        return Request(url=self.user_url, callback=self.parse_user)

    def parse_user(self, response):

        if self.user_id == 400000:
            pass
        else:

            user_name = response.xpath('//*[@id="clm23_main"]/div/div[2]/h2/span/text()').extract_first()
            profile = response.xpath('//*[@id="clm23_main"]/div/div[2]/div[1]/div[1]/ul/li[1]/text()').extract_first()
            user_id = self.user_id
            birth_data = response.xpath('//*[@id="clm23_main"]/div/div[2]/div[1]/div[1]/ul/li[3]/span[2]/text()').extract_first()
            sex = response.xpath('//*[@id="clm23_main"]/div/div[2]/div[1]/div[1]/ul/li[4]/span[2]/text()').extract()
            birthplace = response.xpath('//*[@id="clm23_main"]/div/div[2]/div[1]/div[1]/ul/li[5]/span[2]/text()').extract()
            affiliation = response.xpath('//*[@id="clm23_main"]/div/div[2]/div[1]/div[1]/ul/li[6]/span[2]/text()').extract()
            animes_on_shelf = response.xpath('//*[@id="clm23_main"]/div/div[2]/div[1]/div[1]/ul/li[7]/span[2]/a/text()').extract_first()
            #animes_on_shelf = re.findall('[0-9]+', animes_on_shelf)[0]
            reviews_num = response.xpath('//*[@id="clm23_main"]/div/div[2]/div[1]/div[1]/ul/li[8]/span[2]/a/text()').extract_first()
            #reviews_num = re.findall('[0-9]+', reviews_num)[0]
            thankyou_num = response.xpath('//*[@id="clm23_main"]/div/div[2]/div[1]/div[1]/ul/li[9]/span[2]/text()').extract_first()
            #thankyou_num = re.findall('[0-9]+', thankyou_num)[0]
            more_profile = response.xpath('//*[@id="clm23_main"]/div/div[2]/div[4]/text()').extract()


            l = ItemLoader(item=UserscrapyItem(), response=response)
            l.add_value('user_name', user_name)
            l.add_value('profile', profile)
            l.add_value('user_id', user_id)
            l.add_value('birth_data', birth_data)
            l.add_value('sex', sex)
            l.add_value('birthplace', birthplace)
            l.add_value('affiliation', affiliation)
            l.add_value('animes_on_shelf', animes_on_shelf)
            l.add_value('reviews_num', reviews_num)
            l.add_value('thankyou_num', thankyou_num)
            l.add_value('more_profile', more_profile)

            # print("____________________________________________________")
            # print(self.user_id)

            self.user_id += 1

            # output = {'user_name':user_name, 'profile':profile, 'user_id':user_id, \
            # 'birth_data':birth_data, 'sex':sex, 'birthplace':birthplace, 'affiliation':affiliation,\
            # 'animes_on_shelf':animes_on_shelf, 'reviews_num':reviews_num, 'thankyou_num':thankyou_num,\
            # 'more_profile':more_profile}

            fav_url = response.xpath('//*[@id="clm23_sub"]/div[3]/ul[1]/li[1]/a/@href').extract_first()
            fav_url = response.urljoin(fav_url)


            request = Request(fav_url, callback=self.parse_fav, dont_filter=True)
            request.meta['l'] = l

            if user_name is not None:
                yield request
            else:
                pass

            next_url = 'https://www.anikore.jp/users/profile/' + str(self.user_id) + '/'
            yield Request(next_url, callback=self.parse_user, dont_filter=True)

        

    def parse_fav(self, response):

        request_flag = False

        l = response.meta['l']

        nodes = response.xpath('//td/div[@class="usr-photo"]')
        animes_fav_url = []
        for node in nodes:
            url = node.xpath('./a/@href').extract_first()

            animes_fav_url.append(url)

        next_url = response.xpath('//*[@id="collection"]/div[3]/span[5]/a/@href').extract_first()


        l.add_value('animes_fav_url',  animes_fav_url)


        # pagenate to last page
        if next_url is not None:
             next_url = response.urljoin(next_url)
             request = Request(next_url, callback=self.parse_fav, dont_filter=True)
             request.meta['l'] = l

             yield request
        else:
            request_flag = True

        # only request in last page
        if request_flag == True:

            plan_url = response.xpath('//*[@id="clm23_sub"]/div[3]/ul[1]/li[3]/a/@href').extract_first()
            plan_url = response.urljoin(plan_url)

            request = Request(plan_url, callback=self.parse_plan, dont_filter=True)
            request.meta['l'] = l
            yield request
        else:
            pass


    def parse_plan(self, response):

        request_flag = False

        l = response.meta['l']

        nodes = response.xpath('//td/div[@class="usr-photo"]')
        animes_plan_url = []
        for node in nodes:
            url = node.xpath('./a/@href').extract_first()

            animes_plan_url.append(url)

        l.add_value('animes_plan_url',  animes_plan_url)

        next_url = response.xpath('//*[@id="collection"]/div[3]/span[5]/a/@href').extract_first()


                # pagenate to last page
        if next_url is not None:
             next_url = response.urljoin(next_url)
             request = Request(next_url, callback=self.parse_plan, dont_filter=True)
             request.meta['l'] = l

             yield request
        else:
            request_flag = True

        # only request in last page
        if request_flag == True:
        #go to 
            watching_url = response.xpath('//*[@id="clm23_sub"]/div[3]/ul[1]/li[4]/a/@href').extract_first()
            watching_url = response.urljoin(watching_url)

            request = Request(watching_url, callback=self.parse_watching, dont_filter=True)
            request.meta['l'] = l
            yield request
        else:
            pass

        

    def parse_watching(self, response):

        request_flag = False


        l = response.meta['l']

        nodes = response.xpath('//td/div[@class="usr-photo"]')
        animes_watching_url = []
        for node in nodes:
            url = node.xpath('./a/@href').extract_first()

            animes_watching_url.append(url)

        l.add_value('animes_watching_url',  animes_watching_url)

        next_url = response.xpath('//*[@id="collection"]/div[3]/span[5]/a/@href').extract_first()

        # pagenate to last page
        if next_url is not None:
             next_url = response.urljoin(next_url)
             request = Request(next_url, callback=self.parse_watching, dont_filter=True)
             request.meta['l'] = l

             yield request
        else:
            request_flag = True

        # only request in last page
        if request_flag == True:
            #go to 
            dropped_url = response.xpath('//*[@id="clm23_sub"]/div[3]/ul[1]/li[5]/a/@href').extract_first()
            dropped_url = response.urljoin(dropped_url)

            request = Request(dropped_url, callback=self.parse_dropped, dont_filter=True)
            request.meta['l'] = l
            yield request
        else:
            pass

    def parse_dropped(self, response):

        request_flag = False

        l = response.meta['l']

        nodes = response.xpath('//td/div[@class="usr-photo"]')
        animes_dropped_url = []
        for node in nodes:
            url = node.xpath('./a/@href').extract_first()

            animes_dropped_url.append(url)

        l.add_value('animes_dropped_url',  animes_dropped_url)



        next_url = response.xpath('//*[@id="collection"]/div[3]/span[5]/a/@href').extract_first()
       
        # pagenate to last page
        if next_url is not None:
             next_url = response.urljoin(next_url)
             request = Request(next_url, callback=self.parse_dropped, dont_filter=True)
             request.meta['l'] = l

             yield request
        else:
            request_flag = True

        # only request in last page
        if request_flag == True:
            #go to 
            completed_url = response.xpath('//*[@id="clm23_sub"]/div[3]/ul[1]/li[6]/a/@href').extract_first()
            completed_url = response.urljoin(completed_url)

            request = Request(completed_url, callback=self.parse_completed, dont_filter=True)
            request.meta['l'] = l
            yield request
        else:
            pass




    def parse_completed(self, response):

        request_flag = False

        l = response.meta['l']

        nodes = response.xpath('//div[@class="usr-photo"]')

        animes_completed_url = []
        for node in nodes:
            url = node.xpath('./a/@href').extract_first()

            animes_completed_url.append(url)

        l.add_value('animes_completed_url',  animes_completed_url)

        next_url = response.xpath('//*[@id="collection"]/div[3]/span[5]/a/@href').extract_first()
       

        if next_url is not None:
             next_url = response.urljoin(next_url)
             request = Request(next_url, callback=self.parse_completed, dont_filter=True)
             request.meta['l'] = l

             yield request
        else:
            request_flag = True

        
        if request_flag == True:
            #go to 
            nocategory_url = response.xpath('//*[@id="clm23_sub"]/div[3]/ul[1]/li[7]/a/@href').extract_first()
            nocategory_url = response.urljoin(nocategory_url)
            request = Request(nocategory_url, callback=self.parse_nocategory, dont_filter=True)
            request.meta['l'] = l
            yield request
        else:
            pass

    def parse_nocategory(self, response):

        l = response.meta['l']

        nodes = response.xpath('//td/div[@class="usr-photo"]')
        animes_nocategory_url = []
        for node in nodes:
            url = node.xpath('./a/@href').extract_first()

            animes_nocategory_url.append(url)

        l.add_value('animes_nocategory_url', animes_nocategory_url)
        
        yield l.load_item()
        






        
    

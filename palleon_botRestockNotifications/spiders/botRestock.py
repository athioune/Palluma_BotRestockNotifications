# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
import requests
import json
from scrapy_splash import SplashRequest

class BotRestockSpider(scrapy.Spider):
    name = 'botRestock'
    urlList = ['https://projectdestroyer.com/', 'https://splashforce.io/', 'https://turboaio.com/', 'https://thunder-io.com/', 'https://qbotaio.com/', 'https://t3k.shop/aio-6-months-renewal/', 'https://dashe.io/', 'https://www.theshitbot.com/product/ultimate-sneaker-bot/', 'https://soleaio.com/', 'https://shop.balkobot.com/password', 'https://wrathbots.co/', 'https://kodai.io/', 'https://cybersole.io/', 'https://ghostaio.com/']

    def __init__(self, *args,**kwargs):
        super(BotRestockSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        for url in self.urlList:
            # yield scrapy.Request(url=url, callback=self.parse_id, dont_filter=True)
            yield SplashRequest(url, self.parse_id,
                        )
    def envoiNotif(self, url, accessToken):
        data_send = {"type": "note", "title": "Restock sur {0}".format(url), "body": url}
    
        ACCESS_TOKEN = accessToken
        resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                            headers={'Authorization': 'Bearer ' + ACCESS_TOKEN, 'Content-Type': 'application/json'})
        if resp.status_code != 200:
            raise Exception('Something wrong')

    def parse_id(self, response):
        envoyerMail = False

        if 'splashforce.io' in response.url:
            if 'Sold Out' not in response.body:
                envoyerMail = True
        elif 'projectdestroyer.com' in response.url:
            if 'GET RESTOCK NOTIFICATIONS' not in response.body:
                envoyerMail = True
        elif 't3k.shop' in response.url:
            if 'Out of stock' not in response.body:
                envoyerMail = True
        # elif 'dashe.io' in response.url:
        #     if 'SOLD OUT' not in response.body:
        #         envoyerMail = True
        elif 'theshitbot.com' in response.url:
            if '9,999.00' not in response.body:
                envoyerMail = True
        elif 'soleaio.com' in response.url:
            if 'Sold Out' not in response.body:
                envoyerMail = True
        elif 'balkobot.com' in response.url:
            if 'Stay Tuned' not in response.body:
                envoyerMail = True
        elif 'turboaio.com' in response.url:
            if 'OUT OF STOCK' not in response.body:
                envoyerMail = True
        elif 'thunder-io.com' in response.url:
            if 'Sold Out' not in response.body:
                envoyerMail = True
        elif 'qbotaio.com' in response.url:
            if 'Currently Sold Out' not in response.body:
                envoyerMail = True
        elif 'wrathbots.co' in response.url:
            if 'Out of Stock' not in response.body:
                envoyerMail = True
        elif 'kodai.io' in response.url:
            if 'Currently Sold Out.' not in response.body:
                envoyerMail = True
        elif 'cybersole.io' in response.url:
            if 'Sold Out' not in response.body:
                envoyerMail = True
        elif 'ghostaio.com' in response.url:
            if 'Sold Out' not in response.body:
                envoyerMail = True        

        if envoyerMail:
            self.envoiNotif(response.url, 'SECRET_KEY')

import scrapy


class StocksnewsSpider(scrapy.Spider):
    name = 'StocksNews'
    allowed_domains = ['https://www.infomoney.com.br/ultimas-noticias/']
    start_urls = ['http://https://www.infomoney.com.br/ultimas-noticias//']

    def parse(self, response):
        pass

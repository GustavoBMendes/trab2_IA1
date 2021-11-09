import scrapy


class StocksnewsSpider(scrapy.Spider):
    name = 'StocksNews'
    allowed_domains = ['https://www.infomoney.com.br/ultimas-noticias/']
    start_urls = ['https://www.infomoney.com.br/ultimas-noticias/']

    def parse(self, response):
        for new in response.css('a::text'):
            title = new.get()
            print(title)
        
        yield {'title': title}

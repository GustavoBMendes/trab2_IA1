import scrapy
import investpy as ipy


class StocksnewsSpider(scrapy.Spider):
    name = 'StocksNews'
    #ticker = input('Digite o ticker da ação (exemplo: PETR4): ')
    ticker = 'PETR4'
    
    allowed_domains = ['https://news.google.com/']
    start_urls = ['https://news.google.com/search?q='+ ticker + '&hl=pt-BR&gl=BR&ceid=BR%3Apt-419']

    def parse(self, response):
        stocks_list = Stocks()
        stocks_list.set_stock(self.ticker)
        df = ipy.get_stock_historical_data(stock='PETR4',
                                        country='brazil',
                                        from_date='01/01/2010',
                                        to_date='01/01/2020')
        print(df.head())
        for new in response.css('article div div time::text'):
            title = new.get()
            stocks_list.date_news(title)
        
        yield {'title': title}

class Stocks:
    def __init__(self):
        self.dates_list = []
        self.stock = ''
    
    def date_news(self, date):
        self.dates_list.append(date)
        
    def set_stock(self, stock_name):
        self.stock = stock_name

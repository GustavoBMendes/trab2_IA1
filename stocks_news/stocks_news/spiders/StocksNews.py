import scrapy
import investpy as ipy
import datetime
import operator

class StocksnewsSpider(scrapy.Spider):
    name = 'StocksNews'
    #ticker = input('Digite o ticker da ação (exemplo: PETR4): ')
    ticker = 'PETR4'
    
    allowed_domains = ['https://news.google.com/']
    start_urls = ['https://news.google.com/search?q='+ ticker + '&hl=pt-BR&gl=BR&ceid=BR%3Apt-419']

    def parse(self, response):
        stocks_list = Stocks()
        stocks_list.set_stock(self.ticker)
        for new in response.css('article'):
            date = new.css('div div time::attr(datetime)').get()
            title = new.css('h3 a::text').get()
            stocks_list.set_date_news(date, title)
        news = stocks_list.get_last_news()
        stocks_list.get_stock_info(news)
        #fazer a análise da manchete e classificá - la

class Stocks:
    def __init__(self):
        self.news_list = []
        self.stock = ''
    
    def set_date_news(self, date, title):
        news_dict = {}
        date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').strftime('%d/%m/%Y')
        news_dict['date'] = date
        news_dict['title'] = title
        self.news_list.append(news_dict)
        
    def set_stock(self, stock_name):
        self.stock = stock_name
        
    def get_last_news(self):
        return self.news_list[0]
    
    def get_stock_info(self, news):
        #fazer o range de -2 dias até +2 dias
        date = datetime.datetime.strptime(news['date'], "%d/%m/%Y")
        to_date = date + datetime.timedelta(days=2)
        to_date_str = to_date.strftime('%d/%m/%Y')
        df = ipy.get_stock_historical_data(stock='PETR4',
                                        country='brazil',
                                        from_date=news['date'],
                                        to_date=to_date_str)
        print(df.head())

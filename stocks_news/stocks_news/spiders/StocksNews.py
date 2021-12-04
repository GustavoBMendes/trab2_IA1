import scrapy
import investpy as ipy
import datetime
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

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
        stocks_list.sort_data()
        news = stocks_list.get_last_news()
        #fazer a análise da manchete e classificá - la
        stocks_list.read_csv()
        stocks_list.train_model()
        stocks_list.get_stock_info(news)

class Stocks:
    def __init__(self):
        self.news_list = []
        self.stock = ''
        self.dataset_texts = []
        self.dataset_classes = []
    
    def set_date_news(self, date, title):
        news_dict = {}
        if(title != None):
            date = datetime.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').strftime('%d/%m/%Y')
            date = datetime.datetime.strptime(date,'%d/%m/%Y')
            news_dict['date'] = date
            news_dict['title'] = title
            self.news_list.append(news_dict)
            
    def sort_data(self):
        self.news_list = sorted(self.news_list, key=lambda d: d['date'], reverse=True)
        
    def set_stock(self, stock_name):
        self.stock = stock_name
        
    def get_last_news(self):
        return self.news_list[0]
    
    def get_stock_info(self, news):
        #news = self.news_list
        date_str = datetime.datetime.strftime(news['date'], '%d/%m/%Y')
        date = datetime.datetime.strptime(date_str, "%d/%m/%Y")
        start_date = date - datetime.timedelta(days=2)
        start_date_str = start_date.strftime('%d/%m/%Y')
        end_date = date + datetime.timedelta(days=2)
        end_date_str = end_date.strftime('%d/%m/%Y')
        df = ipy.get_stock_historical_data(stock='PETR4',
                                        country='brazil',
                                        from_date=start_date_str,
                                        to_date=end_date_str)
        #print(df.head())
        print(df.corr())
    
    def read_csv(self):
        dataset = pd.read_csv('./Tweets_Mg.csv',encoding='utf-8')
        self.dataset_texts = dataset["Text"].values
        self.dataset_classes = dataset["Classificacao"].values
    
    def train_model(self):
        vectorizer = CountVectorizer(analyzer = "word")
        freq_tweets = vectorizer.fit_transform(self.dataset_texts)
        
        modelo = MultinomialNB()
        modelo = modelo.fit(freq_tweets, self.dataset_classes)
        
        # Vamos usar algumas frases de teste para fazer a classificação com o modelo treinado
        titles = []
        for new in self.news_list:
            titles.append(new['title'])
            
        freq_testes = vectorizer.transform(titles)
        results = modelo.predict(freq_testes)
        
        for i in range(0, len(self.news_list)):
            self.news_list[i]['classification'] = results[i]
        #print(self.news_list)
        # for new in self.news_list:
        #     if new['classification'] == 'Negativo' or  new['classification'] == 'Positivo':
        #         print(new)
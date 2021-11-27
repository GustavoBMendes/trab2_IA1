from bs4 import BeautifulSoup
import requests

url = 'https://news.google.com/search?q=petr4&hl=pt-BR&gl=BR&ceid=BR%3Apt-419'
res = requests.get(url)
html_page = res.text
soup = BeautifulSoup(html_page, 'html.parser')
soup.prettify()
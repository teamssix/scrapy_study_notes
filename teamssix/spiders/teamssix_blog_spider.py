import scrapy
from bs4 import BeautifulSoup
from teamssix.items import TeamssixItem

class BlogSpider(scrapy.Spider):

	name = 'blogurl'
	start_urls = [
		'https://www.teamssix.com',
		'https://www.teamssix.com/page/2/',
		'https://www.teamssix.com/page/3/',
		'https://www.teamssix.com/page/4/',
		'https://www.teamssix.com/page/5/'
	]
	custom_settings = {'LOG_LEVEL': 'ERROR'}
	def parse(self,response):
		soup = BeautifulSoup(response.text,'html.parser')
		for i in soup.select('.post-title'):
			url = 'https://www.teamssix.com{}'.format(i['href'])
			yield scrapy.Request(url,callback=self.sub_article)

	def sub_article(self,response):
		soup = BeautifulSoup(response.text,'html.parser')
		title = self.article_title(soup)
		list = self.article_list(soup)
		print(title)
		item = TeamssixItem(_id = response.url,title = title,list = list)
		yield item

		soup = BeautifulSoup(response.text, 'html.parser')
		for i in soup.select('.post-title'):
			url = 'https://www.teamssix.com{}'.format(i['href'])
			yield scrapy.Request(url, callback=self.sub_article)


	def article_title(self,soup):
		return soup.select('.title')[0].text

	def article_list(self,soup):
		list = []
		for i in soup.select('.toc-text'):
			list.append(i.text)
		return list

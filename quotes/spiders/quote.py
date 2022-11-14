import scrapy
from .config import API
from scraper_api import ScraperAPIClient
client = ScraperAPIClient(API)
import time


class QuoteSpider(scrapy.Spider):
    name = 'quote'
    # start_urls = [client.scrapyGet(url = 'https://www.brainyquote.com')]
    
    def urllist():
        url_list = []
        latters = 'xyz'
        b_url = 'https://www.brainyquote.com/authors/'
        for l in latters:
            url = b_url + l
            url_list.append(url)
        return url_list
    url_list = urllist()
    
    def start_requests(self):
        for url in self.url_list:
            time.sleep(2)
            yield scrapy.Request(client.scrapyGet(url=url))
    
    def parse(self, response):
        rows = response.css('table.table.table-hover.table-bordered tbody tr')
        for row in rows:
            baseurl = 'https://www.brainyquote.com'
            tailurl = row.css('td a::attr(href)').get() 
            url = baseurl+tailurl
            yield scrapy.Request(client.scrapyGet(url=url), callback= self.quotes)
        
        next_author = response.css('li.page-item a.page-link:contains(Next)::attr(href)').get()
        baseurl = 'https://www.brainyquote.com'
        
        if next_author is not None:
            m_url = baseurl+next_author
            yield scrapy.Request(client.scrapyGet(url=m_url), callback=self.parse)
        
        
    def quotes(self, response):
        name = response.css('h1.bq-subnav-h1::text').get().strip().replace(' Quotes', '')
        if name == '':
            name = response.css('h1 a.bq-subnav-lnk::text').get().strip().replace(' Quotes', '')
        nationality = response.css('div.subnav-below-p a::text').get()
        profession = response.css('div.subnav-below-p a:nth-child(n+2)::text').get()
        wiki_profile = response.css('a[target="wikipedia"]::attr(href)').get()
        rows = response.css('div.grid-item.qb')
        for row in rows:
            quotes = row.css('a.b-qt div::text').get().strip()
            url = 'https://www.brainyquote.com'
            quotes_link = url+row.css('a::attr(href)').get().strip()
            data = {
                'Quotes': quotes,
                'Name': name,
                'Nationality': nationality,
                'Profession': profession,
                'Quote_link': quotes_link,
                'Wiki_Profile': wiki_profile
            }
            yield data
        next_author = response.css('li.page-item a.page-link:contains(Next)::attr(href)').get()
        baseurl = 'https://www.brainyquote.com'
        
        
        if next_author is not None:
            m_url = baseurl+next_author
            yield scrapy.Request(client.scrapyGet(url=m_url), callback=self.quotes)

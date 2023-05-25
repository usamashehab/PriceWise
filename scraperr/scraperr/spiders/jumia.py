import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from items import clean_price, get_description
import re
class JumiaSpider(CrawlSpider):
    name = 'jumia'
    allowed_domains = ['jumia.com.eg']
    start_urls = [
        'https://www.jumia.com.eg/', \
        'https://www.jumia.com.eg/mobile-phones/',
        'https://www.jumia.com.eg/traditional-laptops/',
        'https://www.jumia.com.eg/televisions/',
        'https://www.jumia.com.eg/tablets/',
        ]

    rules = (
        Rule(LinkExtractor(allow =r'mobile-phones\/\?page=\d+#catalog-listing', unique=True), follow=True, callback='parse_page', cb_kwargs={'category': 'Mobile'}),
        Rule(LinkExtractor(allow =[r'traditional-laptops\/\?page=\d+#catalog-listing', r'gaming-laptops\/\?page=\d+#catalog-listing', r'2-in-1-laptops'], unique=True), follow=True, callback='parse_page', cb_kwargs={'category': 'Laptop'}),
        Rule(LinkExtractor(allow =r'televisions\/\?page=\d+#catalog-listing', unique=True), follow=True, callback='parse_page', cb_kwargs={'category': 'TV'}),
        Rule(LinkExtractor(allow =r'tablets\/\?page=\d+#catalog-listing', unique=True), follow=True, callback='parse_page', cb_kwargs={'category': 'Tablet'}),
    )

    def parse_page(self, response, category):
        for card in response.css('.c-prd'):
            url = card.css('.c-prd a.core::attr(href)').get()            
            yield scrapy.Request(url=url, callback=self.parse_product, cb_kwargs={'category': category})
    
    def parse_product(self, response, category):
        item = {}
        title = response.css('.-fs20.-pbxs ::text').get()
        item['uid'] = re.search(r'-(\w*)\.html', response.url).group(1)
        item['title'] = title
        item['url'] = response.url
        old_price = response.css('.-mtxs .-i-ctr ::text').get(default=None)
        if old_price:
            item['sale_price'] = clean_price(response.css('.-fs24 ::text').get(default=None))
            item['price'] = old_price
        else:
            item['price'] = clean_price(response.css('.-fs24 ::text').get(default=None))
            item['sale_price'] = None
        item['brand'] = title.split(' ')[0]
        item['vendor'] = 'Jumia'
        item['category'] = category
        item['is_product']=True
        item['description'] = get_description(response.css('.-sc ::text').getall())
        # item['specs'] = response.css('.product-specs ::text').get(default=None)
        yield item

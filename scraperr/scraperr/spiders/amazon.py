from urllib.parse import urlencode
import scrapy
import logging
from collections import namedtuple
import re
from ..items import (
    handle_product_variations,
    get_price,
    get_product_details,
    get_product_images,
    get_description,
    get_ram_from
    )
from twisted.internet import defer

API_KEY = '466936c8-7e96-4334-9d26-31628a7688b1'

def get_scrapeops_url(url):
    # scrape_ops_url = 'https://proxy.scrapeops.io/v1/?'
    # params = {'api_key': API_KEY, 'url': url}
    # return scrape_ops_url + urlencode(params)
    return url

class AmazonSpSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.eg', 'proxy.scrapeops.io']

    # starts requests to the major categories
    def start_requests(self):
        category = namedtuple('category', ['name', 'url'])
        categories = [
            category('Mobile', 'https://www.amazon.eg/-/en/s?i=electronics&bbn=21832883031&rh=n%3A21832883031%2Cp_n_feature_seven_browse-bin%3A27088055031%7C27088056031&dc&fs=true&page={}&language=en&qid=1678985625&rnid=27088044031&ref=sr_pg_2'),
            category('TV', 'https://www.amazon.eg/s?i=electronics&bbn=21832982031&rh=n%3A21832982031%2Cp_n_feature_eight_browse-bin%3A22080630031%7C22080631031%7C22080632031%7C22080634031&dc&language=en&ds=v1%3ALp9%2BJqkp2zC6tZ%2ByElhAvpF5ldXdJzYEWkFdgAJh1ns&qid=1681759812&rnid=22080628031&ref=sr_nr_p_n_feature_eight_browse-bin_4'),
            category('Laptop', 'https://www.amazon.eg/-/en/s?i=electronics&bbn=21832907031&rh=n%3A18018102031%2Cn%3A21832872031%2Cn%3A21832907031&dc&fs=true&language=en&qid=1683572938&ref=sr_pg_1'),
            category('Tablet', 'https://www.amazon.eg/s?i=electronics&bbn=21832915031&rh=n%3A21832915031%2Cp_n_feature_thirteen_browse-bin%3A27906366031%7C27906367031%7C27906368031%7C27906369031%7C27906370031%7C27906371031%7C27906372031%7C27906373031%7C27906374031&dc&fs=true&language=en&ds=v1%3APNG6RFVefOU76fddzrhg6TDL4hkNpkSjfQQUpY7MzrE&qid=1684002177&rnid=27906365031&ref=sr_nr_p_n_feature_thirteen_browse-bin_9'),

            ]
        for cat in categories:
            yield scrapy.Request(url=get_scrapeops_url(cat.url), callback=self.do_pagination, cb_kwargs={'category':cat.name, 'url':cat.url})

    # send requests to each category pages
    def do_pagination(self, response, category, url):
        total_pages = response.css('.s-pagination-item ::text').getall()[-2] 
        current_page = response.css('.s-pagination-selected ::text').get()
        if current_page and total_pages:
            if int(current_page)==1:
                for i in range(int(total_pages)+1):
                    next_page = url.replace('language=en', f'page={i}&language=en')
                    yield scrapy.Request(url=get_scrapeops_url(next_page), callback=self.parse_page, cb_kwargs={'category':category})

    # parse the products page
    def parse_page(self, response, category):
        for card in response.css('.s-card-border'):
            product_link = card.css('.s-line-clamp-4 a::attr(href)').get()
            product_link = 'https://www.amazon.eg'+ product_link
            id = re.search(r'B0\w{8}', product_link).group(0)
            price_string = response.css('.a-row.a-color-base').get()
            yield scrapy.Request(url=get_scrapeops_url(product_link), callback=self.parse_product_data, cb_kwargs={'category':category, 'id':  id, 'price_string': price_string})

    # parses a product page
    def parse_product_data(self, response, **kwargs):
        item = {}
        about_details = get_product_details(response.css('#poExpander td ::text').getall())
        description = get_description(response.css('#productDescription span::text').getall())
        category = kwargs.get('category')
        uid = kwargs.get('id')
        title = response.css('#productTitle ::text').get(default='').strip()
        item['uid'] = uid
        item['sale_price'], item['price'] = get_price(kwargs.get('price_string'))
        item['url'] = 'https://www.amazon.eg/dp/'+ uid
        item['title'] = title
        item['brand'] = about_details.get('Brand')
        item['description'] = description
        item['available'] = True if item['price'] is not None else False
        item['category'] = category
        item['vendor'] = 'Amazon'
        item['is_product']=True
        yield  item
        if category not in ['Mobile', 'TV', 'Laptop', 'Tablet']:
            return
        technical_details = get_product_details(response.css('#productDetails_techSpec_section_1 .a-size-base ::text').getall())

        details = {
            'uid': item['uid'],
            'title': item['title'],
            'category': item['category'],
            'about_details': about_details,
            'technical_details': technical_details,
            'description' : description,
            'images_ids': get_product_images(response.css('.regularAltImageViewLayout img::attr(src)').getall())
        }
        yield from self.parse_product_details(details)

    @handle_product_variations
    def parse_product_details(self, details): 
        # logging.info(f'parsing product details for {item.get("uid")}')
        yield details

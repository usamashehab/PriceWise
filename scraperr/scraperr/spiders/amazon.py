from urllib.parse import urlencode
import scrapy
from collections import namedtuple
import re
from ..items import (
    handle_product_variations,
    get_price,
    get_product_details,
    get_product_images,
    get_brands,
    fetch_brand,
    )

API_KEY = '17ac39eb-1278-4af9-9205-73eeab7112e1'

def get_scrapeops_url(url):
    scrape_ops_url = 'https://proxy.scrapeops.io/v1/?'
    params = {'api_key': API_KEY, 'url': url}
    return scrape_ops_url + urlencode(params)

class AmazonSpSpider(scrapy.Spider):
    name = 'amazon'
    allowed_domains = ['amazon.eg', 'proxy.scrapeops.io']

    # starts requests to the major categories
    def start_requests(self):
        category = namedtuple('category', ['name', 'url'])
        categories = [
            # category('Mobile', 'https://www.amazon.eg/-/en/s?i=electronics&bbn=21832883031&rh=n%3A21832883031%2Cp_n_feature_seven_browse-bin%3A27088055031%7C27088056031&dc&fs=true&page={}&language=en&qid=1678985625&rnid=27088044031&ref=sr_pg_2'),
            category('TV', 'https://www.amazon.eg/s?i=electronics&bbn=21832982031&rh=n%3A21832982031%2Cp_n_feature_eight_browse-bin%3A22080630031%7C22080631031%7C22080632031%7C22080634031&dc&language=en&ds=v1%3ALp9%2BJqkp2zC6tZ%2ByElhAvpF5ldXdJzYEWkFdgAJh1ns&qid=1681759812&rnid=22080628031&ref=sr_nr_p_n_feature_eight_browse-bin_4'),
            ]
        for cat in categories:
            yield scrapy.Request(url=get_scrapeops_url(cat.url), callback=self.do_pagination, cb_kwargs={'category':cat.name, 'url':cat.url})

    # send requests to each category pages
    def do_pagination(self, response, category, url):
        total_pages = response.css('.s-pagination-disabled::text').getall()[-1]
        current_page = response.css('.s-pagination-selected::text').get()
        if current_page and total_pages:
            if int(current_page)==1:
                for i in range(2, int(total_pages)+1):
                    next_page = url.replace('language=en', f'page={i}&language=en')
                    yield scrapy.Request(url=get_scrapeops_url(next_page), callback=self.parse_page, cb_kwargs={'category':category})

    # parse the products page
    def parse_page(self, response, category):
        brands = get_brands(response.css('#brandsRefinements .a-spacing-micro').getall())
        for card in response.css('.s-card-border'):
            item = {}
            product_link = card.css('.s-line-clamp-4 a::attr(href)').get()
            id = re.search(r'B0\w{8}', product_link).group(0)
            price_string = card.css('.a-row.a-color-base').get()
            item['uid'] = id
            item['sale_price'], item['price'] = get_price(price_string)
            item['url'] = 'https://www.amazon.eg/'+ product_link
            item['title'] = card.css('.a-size-base-plus::text').get()
            item['brand'] = fetch_brand(item['title'], brands)
            item['available'] = True if card.css('.a-price-whole::text').get() else False
            item['category'] = category
            item['vendor'] = 'Amazon'
            item['is_product']=True
            yield item
            yield scrapy.Request(url=get_scrapeops_url(item['url']), callback=self.parse_product_data, cb_kwargs={'category':category, 'id':  id})

    # parses a product page
    @handle_product_variations 
    def parse_product_data(self, response, **kwargs):
        about_details = get_product_details(response.css('#poExpander td ::text').getall())
        technical_details = get_product_details(response.css('#productDetails_techSpec_section_1 .a-size-base ::text').getall())
        title = response.css('#productTitle::text').get().strip()
        description = response.css('#productDetails_techSpec_section_1 .a-size-base ::text')
        item = {
            'category': kwargs.get('category'),
            'title' : title,
            'about_details': about_details,
            'technical_details': technical_details,
            'description' : description,
            'images_ids': get_product_images(response.css('.regularAltImageViewLayout img::attr(src)').getall())
        }
        yield item

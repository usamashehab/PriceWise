from scrapy_djangoitem import DjangoItem
from product.models.product import Product, Price, Image 
from w3lib.html import remove_tags
import re

def get_price(price_tag):
    """
    Extracts sale_price and price if exist

    args:
        price_tag: the html tag that holds price
    Returns:
        list of prices 
    """
    if price_tag is None:
        return [None, None]
    price_str = remove_tags(price_tag)
    price_str = price_str.strip().replace(',', '')
    prices = re.findall(r"EGP([0-9]*\.[0-9]*)", price_str)
    if len(prices)==2:
        return prices
    else:
        return [None, prices[0]]

def get_product_details(details_list):
    """
    Transforms amaozn product details list to  dict

    args:
        details_table : List of strings 
    Return:
        dict
    """
    details= [item.strip().replace('\u200e','') for item in details_list]
    details = [i for i in details if i]
    return {details[i]: details[i+1] for i in range(0, len(details), 2)}

def get_product_images(imags_links_list):
    """
    Takes out the ids of the images 'src="https://m.media-amazon.com/images/I/-->41lTVOcW06L._AC_US40_<--.jpg'

    args:
    imgs_links_list: list of images links

    Returns:
    list of string (ids)
    """
    return re.findall(r'I\/(.*?)\.', ''.join(imags_links_list))

features = {'mobile phones': ['Operating system', 'Memory storage capacity', 'Screen size', 'RAM'],
                'laptops': ['Standing screen display size', 'Resolution', 'Processor Brand', 'Processor Type', 'Processor Speed',\
                            'Hard Disk Description', 'Resolution', \
                            'Operating System', 'Installed RAM memory size', 'Memory Technology'],
                'Tvs': ['Screen size', 'Display technology', 'Resolution', 'Refresh rate']}
def handle_product_variations(func):
    def wrapper(*args, **kwargs):
        result = next(func(*args, **kwargs))
        category = kwargs['category']
        features_list = features[category]
        about_dict = result['about_details']
        technical_details = result['technical_details']
        result_dict = about_dict
        result_dict.update(technical_details)
        for feature in features_list:
            if feature in result_dict:
                result_dict[feature] = result_dict.get(feature)
            else :
                result_dict[feature] = None
        filtered_result = {k: v for k, v in result_dict.items() if k in features_list}
        filtered_result['images_ids'] = result['images_ids']
        filtered_result['id'] = result['product_id']        
        return filtered_result
    return wrapper

def get_brands(brand_tags):
    """
    Transforms a list of tags to just the list of brands
    
    args:
    brand_tags: list of string
    
    Returns:
    list"""
    brands=[]
    for brand in brand_tags:
        brands.append(remove_tags(brand).replace('\n','').replace(' ',''))
    return brands

def fetch_brand(title, brand_list):
    """
    Extracts product brand from its title
    
    args:
    title: product title str
    brand_list: str list 
    
    Returns:
    str
    """
    for brand in brand_list:
        if brand.lower() in title.lower():
            return brand
        else:
            return None


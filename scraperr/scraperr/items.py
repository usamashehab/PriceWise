from scrapy_djangoitem import DjangoItem
from product.models.core import Mobile, TV, Laptop 
from w3lib.html import remove_tags
import requests
import re

def get_price(price_tag):
    """
    Extracts sale_price and price if exist

    args:
        price_tag: the html tag that holds price
    Returns:
        list of float 
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
    Takes out the ids of the images 'src="https://m.media-amazon.com/images/I/-->41lTVOcW06L<--.jpg'

    args:
    imgs_links_list: list of images links

    Returns:
    list of string (ids)
    """
    return re.findall(r'I\/(.*?)\.', ''.join(imags_links_list))

features = {
    'Mobile': ['Model name','Operating system', 'Memory storage capacity', 'Screen size', 'RAM', \
               'Connectivity technology', 'Brand'],
    'Laptop': ['Model name', 'Standing screen display size', 'Resolution', \
                'Processor Brand', 'Processor Type', 'Processor Speed', 'Processor Count', \
                'Hard Disk Description', 'Installed RAM memory size', 'Memory Technology', \
                'Operating System', 'Brand'
                ],
    'TV':['Model name', 'Screen size', 'Display technology', 'Resolution', 'Refresh rate', \
        'Connectivity technology', 'Brand']
}
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
        filtered_result = prepare_item(filtered_result, category)
        filtered_result['images_ids'] = result['images_ids']
        filtered_result['uid'] = result['uid']
        filtered_result['category'] = kwargs['category']
        filtered_result['description'] = result['description']
        filtered_result['vendor'] = 'Amazon'
        filtered_result['is_product'] = False
        return filtered_result
    return wrapper

model_map={
    'Mobile':{
        # MainFields
        'Model name' : 'model',
        # Operating system
        'Operating system': 'operating_system',
        'Os': 'operating_system',
        # Connectivity
        'Connectivity technology': 'connectivity_tech',
        # Generak Storage
        'Memory storage capacity':'storage',
        'RAM': 'ram',
        # Display
        'Screen size': 'screen_szie'
        },
    'Laptop':{
        # MainFields
        'Model name' : 'model',
        # Operating system
        'Operating system': 'operating_system',
        'Os': 'operating_system',
        # Connectivity
        'Connectivity technology': 'connectivity_tech',
        # Generak Storage
        'Memory storage capacity':'storage',
        'Hard Disk Description':'storage_type',
        'RAM': 'ram',
        'Memory Technology': 'ram_type',
        # Display
        'Standing screen display size': 'display_size',
        'Resolution' : 'display_resolution',
        # Processor
        'Processor Brand' : 'cpu_brand',
        'Processor Type':'cpu_type',
        'Processor Speed': 'cpu_speed',
        'Processor Count' : 'cpu_num_cores'
    },
    'TV': {
        # MainFields
        'Model name' : 'model',
        # Connectivity
        'Connectivity technology': 'connectivity_tech',
        # Display
        'Screen size': 'screen_size',
        'Display technology' : 'display_type',
        'Resolution' : 'display_resolution',
        'Refresh rate' : 'refresh_rate'
    }
}
def prepare_item(item: dict, category: str):
    """
    prepares item keys to the specified Model
    
    args:
        item: dict of scrapped item
        category: str 
    
    Returns:
        dict ready for models
    """
    mapper = model_map[category]
    for scraped_field, model_field in mapper.items():
            if scraped_field in item:
                value = item.get(scraped_field)
                item[model_field] = value
                del item[scraped_field]
    return item

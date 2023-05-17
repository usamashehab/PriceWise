from scrapy_djangoitem import DjangoItem
from product.models.core import Mobile, TV, Laptop, Tablet
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
    if isinstance(prices, list):
        if len(prices)==2:
            return prices
        else:
            return [None, prices[0]]
    else:
        return [None, prices]   

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

def get_description(description):
    """
    Takes care of either the description is a list, string or None
    
    args: list of strigs
    Returns: str
    """
    if description is None:
        return 'No Description'
    elif isinstance(description, list):
        return ' '.join(description).strip()
    else:
        return description.strip()


features = {
    'Mobile': ['Model name','Operating system', 'OS','Memory storage capacity', 'Screen size', 'Installed RAM memory size', 'RAM', \
               'Connectivity technology', 'Wireless network technology', 'Connectivity technologies'],
    'Laptop': ['Series', 'Standing screen display size', 'Resolution', \
                'Processor Brand', 'Processor Type', 'Processor Speed', 'Processor Count', \
                'Hard Disk Description', 'Installed RAM memory size', 'RAM Size','Memory Technology', \
                'Graphics Chipset Brand' , 'Graphics Coprocessor', 'Graphics Card Ram Size', \
                'Hard disk size', 
                'Operating System', 'Lithium Battery Energy Content'],
    'TV':['Model name', 'Screen size', 'Display technology', 'Resolution', 'Refresh rate', \
        'Connectivity technology'],
    'Tablet':['Series', 'Operating System', \
        'Standing screen display size', 'Screen size', \
        'Installed RAM memory size', 'RAM Size', 'Memory storage capacity',\
        'Connectivity type', 'Battery life'],
}


def handle_product_variations(func):
    def wrapper(*args, **kwargs):
        result = next(func(*args, **kwargs))
        category = result['category']
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
        filtered_result['title'] = result['title']
        filtered_result = prepare_item(filtered_result, category)
        filtered_result['images_ids'] = result['images_ids']
        filtered_result['uid'] = result['uid']
        filtered_result['category'] = category
        filtered_result['vendor'] = 'Amazon'
        filtered_result['is_product'] = False
        yield filtered_result
    return wrapper

model_map={
    'Mobile':{
        # MainFields
        'Model name' : 'model_name',
        # Operating system
        'OS': 'operating_system',
        'Operating system': 'operating_system',
        # Connectivity
        'Wireless network technology' : 'connectivity_tech',
        'Connectivity technology': 'connectivity_tech',
        'Connectivity technologies': 'connectivity_tech',
        # General Storage
        'Memory storage capacity':'storage',
        'Installed RAM memory size': 'ram',
        'RAM': 'ram',
        # Display
        'Screen size': 'display_size'
        },
    'Laptop':{
        # MainFields
        'Series' : 'model_name',
        # Operating system
        'Operating System': 'operating_system',
        'OS': 'operating_system',
        # Connectivity
        'Connectivity technology': 'connectivity_tech',
        # Generak Storage
        'Memory storage capacity':'storage',
        'Hard disk size':'storage',
        'Hard Disk Description':'storage_type',
        'RAM': 'ram',
        'Installed RAM memory size': 'ram',
        'RAM Size': 'ram',
        'Memory Technology': 'ram_type',
        # Display
        'Standing screen display size': 'display_size',
        'Resolution' : 'display_resolution',
        # Processor
        'Processor Brand' : 'cpu_brand',
        'Processor Type':'cpu_type',
        'Processor Speed': 'cpu_speed',
        'Processor Count' : 'cpu_num_cores',
        # Graphics
        'Graphics Chipset Brand' : 'gpu_brand',
        'Graphics Coprocessor' : 'gpu_coprocessor',
        'Graphics Card Ram Size' : 'gpu_memory',
        # Battery
        'Lithium Battery Energy Content' : 'battery_life'
    },
    'TV': {
        # MainFields
        'Model name': 'model_name',
        # Connectivity
        'Connectivity technology': 'connectivity_tech',
        # Display
        'Screen size': 'display_size',
        'Display technology' : 'display_type',
        'Resolution' : 'display_resolution',
        'Refresh rate' : 'refresh_rate',
        # Model Fields
        'Supported Internet services' : 'smart_tv'
    },
    'Tablet':{
        # MainFields
        'Series' : 'model_name',
        # Operating system
        'Operating System': 'operating_system',
        # Connectivity
        'Connectivity type': 'connectivity_tech',
        # General Storage
        'Memory storage capacity':'storage',
        'RAM Size': 'ram',
        'Installed RAM memory size': 'ram',
        # Display
        'Standing screen display size': 'display_size',
        'Screen size': 'display_size',
        # Battery
        'Battery life': 'battery_life'
    },
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
                if category in ['Mobile', 'Laptop', 'Tablet'] and model_field == 'ram':
                    if value is None:
                        value = get_ram_from(item['title'])
                    else:
                        value = get_ram_from(value)
                    if value is not None:
                        if value < 1:
                            value = 1
                        if value > 32:
                            value = 8
                if category in ['Mobile', 'Laptop', 'Tablet'] and model_field == 'storage':
                    if value is None:
                        value = get_storage_from(item['title'])
                    else:
                        value = get_storage_from(value)
                item[model_field] = value
                del item[scraped_field]
    item.pop('title')
    return item


def get_ram_from(title):
    """Takes out the ram value from the given text in GBs using regex
    arg
        title: str
    return
        ram: str or None
    """
    extracted_values = re.findall(r'(\d*\.?\d*) ?([GM]B)', title)
    if extracted_values:
        ram_values = [float(value) /(1024.0 if unit == 'M' else 1) for value, unit in extracted_values]
        return min(ram_values)
    else:
        return None

def get_storage_from(title):
    """Takes out the storage value from the given text using regex in GBs
    arg
        title: str
    return
        storage: str or None
    """
    extracted_values = re.findall(r'(\d*\.?\d*) ?([GT]B)', title)
    if extracted_values:
        storage_values = [float(value) * (1024 if unit == 'TB' else 1) for value, unit in extracted_values]
        return max(storage_values)
    else:
        return None


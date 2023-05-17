from product.models.product import (Product,
                                    Image)
from product.models.core import(Mobile,
                                Laptop,
                                TV,
                                Tablet)
from product.models.category import Category
from product.models.vendor import Vendor
import scrapy
import logging


category_model_map = {
    'Mobile': Mobile,
    'Laptop': Laptop,
    'TV': TV,
    'Tablet': Tablet,
}

class ProductPipeline:
    # def open_spider(self):
    #     pass

    def process_item(self, item, spider):
        # if empty item
        if not any(item.values()):
            logging.info('emtpy')
            return

        if item['is_product']:
            item.pop('is_product')
            logging.info(f"Creating or updating Model for Item {item['uid']}")
            product, created = Product.objects.create_or_update(**item)
            if not created:
                # just updated the product price history
                return product
        else:
            #  Store Product images
            item.pop('is_product')
            vendor = Vendor.objects.get(name=item.pop('vendor'))
            uid = item.pop('uid')
            product = Product.objects.get(uid=uid, vendor=vendor)
            if Image.objects.filter(product=product).exists():
                # if images already exists for the product
                logging.info("Image already exists for the product")
                item.pop('images_ids')
            else:
                for order, image in enumerate(item.pop('images_ids')):
                    img, created = Image.objects.get_or_create(
                        product = product,
                        image_url = image,
                        order=order
                    )
                    if created:
                        img.save()

            # Store product details in the related model -->TV, Laptpo etc
            item['product'] = product
            category = item.pop('category')
            model = category_model_map[category]
            logging.info(f"Saving {uid} in {category} table")
            related_model, is_created = model.objects.get_or_create(**item)
            if is_created:
                related_model.save()
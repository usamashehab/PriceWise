from product.models.product import (Product,
                                    Image)
from product.models.core import (Mobile,
                                 Laptop,
                                 Tablet,
                                 TV)
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
            # Store Product images
            item.pop('is_product')
            vendor = Vendor.objects.get(name=item.pop('vendor'))
            uid = item.pop('uid')
            product = Product.objects.filter(uid=uid, vendor=vendor).first()
            for order, image in enumerate(item.pop('images_ids')):
                img, created = Image.objects.get_or_create(
                    product=product,
                    image_url=image,
                    order=order
                )
                if created:
                    img.save()
            # update brand and description for the product
            try:
                brand = item.pop('brand')
                description = item.pop('description')
                logging.info(
                    f"Item {uid} Trying to update brand and description")
                Product.objects.filter(uid=uid, vendor=vendor).update(
                    brand=brand, description=description)
            except Product.DoesNotExist:
                pass

            # Store product details in the related model -->TV, Laptpo etc
            item['product'] = product
            category = item.pop('category')
            model = category_model_map[category]
            logging.info(f"Saving {uid} in {category} table")
            related_model, is_created = model.objects.get_or_create(**item)
            if is_created:
                related_model.save()

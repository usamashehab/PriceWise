from product.models.product import (Product,
                                    Image)
from product.models.core import(Mobile,
                                Laptop,
                                TV)
from product.models.category import Category
from product.models.vendor import Vendor
import scrapy


category_model_map = {
    'Mobile': Mobile,
    'Laptop': Laptop,
    'TV': TV
}

class ProductPipeline:

    def process_item(self, item, spider):
        # category = Category.objects.get(name='Mobile')
        # vendor = Vendor.objects.get(name=item['vendor'])
        if item['is_product']:
            item.pop('is_product')
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
            model = category_model_map[item.pop('category')]
            for order, image in enumerate(item.pop('images_ids')):
                img, created = Image.objects.get_or_create(
                    product = product,
                    image_url = image,
                    order=order
                )
                if created:
                    img.save()
            # update brand and description for the product
            try:
                brand = item.pop('Brand')
                description = item.pop('description')
                Product.objects.filter(uid=uid, vendor=vendor).update(brand=brand, description=description)
            except Product.DoesNotExist:
                pass

            # Store product details in the related model -->TV, Laptpo etc
            item['product'] = product
            model, created = model.objects.get_or_create(**item)
            if created:
                model.save()
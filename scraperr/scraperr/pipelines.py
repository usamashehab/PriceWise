from product.models.product import (Product,
                                    ProductManager,
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
            product, created = Product.objects.create_or_update(**item)
            if not created:
                # just updated the product price history
                return product
        else:
            #  Add the images and details model
            images = item.pop('images_ids')
            model = category_model_map[item.pop('category')]
            for order, image in enumerate(images):
                img, created= Image.objects.get_or_create(
                    product = product,
                    image_url = image,
                    order=order
                )
                if created:
                    img.save()
            item['product'] = product
            model, created = model.objects.get_or_create(**item)
            if created:
                model.save()
            # update brand and description for the product
            uid = item.pop['uid']
            vendor = Vendor.objects.get(name=item.pop('vendor'))
            try:
                product = Product.objects.get(uid=uid, vendor=vendor)
                if product.brand != item['Brand']:
                    product.brand = item['Brand']
                if product.description != item['description']:
                    product.description = item['description']
                product.save()
            except Product.DoesNotExist:
                pass
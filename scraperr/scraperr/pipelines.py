from product.models.product import (Product,
                                    ProductManager,
                                    Image)
from product.models.core import(Mobile,
                                Laptop,
                                TV)
# from product.models.category import Category
# from product.models.vendor import Vendor
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
                return product
            else:
                images = item.pop('images_ids')
                model = category_model_map[item.pop('category')]
                for order, image in enumerate(images):
                    i = Image.objects.create(
                        product = product,
                        image_url = image,
                        order=order
                    )
                    i.save()
                item['product'] = product
                model = model.objects.create(**item)
                model.save()
                return product, item
        else:
            pass
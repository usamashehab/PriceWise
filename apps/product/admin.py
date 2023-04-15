from django.contrib import admin
from .models import (
    Product,
    Vendor,
    Category,
    Mobile,
    TV,
    Tablet,
    Laptop
)
# Register your models here.

admin.site.register(Product)
admin.site.register(Vendor)
admin.site.register(Category)
admin.site.register(Mobile)
admin.site.register(TV)
admin.site.register(Tablet)
admin.site.register(Laptop)

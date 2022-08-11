from django.contrib import admin
from .models import MainCatalogModel,SubCatalogModel,ProductModel


# Register your models here.
admin.site.register(MainCatalogModel)
admin.site.register(SubCatalogModel)
admin.site.register(ProductModel)
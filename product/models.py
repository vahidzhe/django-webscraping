from django.db import models

# Create your models here.
class MainCatalogModel(models.Model):
    name = models.CharField(max_length=50,unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    change_date = models.DateTimeField(auto_now=True)

    class Meta:
        # db_table = 'main_catalog'
        verbose_name = 'Ana Katalog'
        verbose_name_plural = 'Ana Kataloglar'

    def __str__(self):
        return self.name

class SubCatalogModel(models.Model):
    name = models.CharField(max_length=50,unique=True)
    main_catalog = models.ForeignKey(MainCatalogModel,on_delete=models.CASCADE,related_name='subcatalogs')
    created_date = models.DateTimeField(auto_now_add=True)
    change_date = models.DateTimeField(auto_now=True)


    class Meta:
        # db_table = 'sub_catalog'
        verbose_name = 'Alt Katalog'
        verbose_name_plural = 'Alt Kataloglar'

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    name = models.CharField(unique=True,max_length=50)
    catalog = models.ManyToManyField(SubCatalogModel,related_name= 'products')
    price = models.FloatField()
    old_price = models.FloatField()
    created_date = models.DateTimeField(auto_now_add=True)
    change_date = models.DateTimeField(auto_now=True)


    class Meta:
        # db_table = 'product'
        verbose_name = 'Məhsul'
        verbose_name_plural = 'Məhsullar'

    def __str__(self):
        return self.name


        
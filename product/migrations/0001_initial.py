# Generated by Django 3.2 on 2022-08-02 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MainCatalogModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('change_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Ana Katalog',
                'verbose_name_plural': 'Ana Kataloglar',
                'db_table': 'main_catalog',
            },
        ),
        migrations.CreateModel(
            name='SubCatalogModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('change_date', models.DateTimeField(auto_now=True)),
                ('main_catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcatalogs', to='product.maincatalogmodel')),
            ],
            options={
                'verbose_name': 'Alt Katalog',
                'verbose_name_plural': 'Alt Kataloglar',
                'db_table': 'sub_catalog',
            },
        ),
        migrations.CreateModel(
            name='ProductModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('price', models.PositiveIntegerField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('change_date', models.DateTimeField(auto_now=True)),
                ('catalog', models.ManyToManyField(related_name='products', to='product.SubCatalogModel')),
            ],
            options={
                'verbose_name': 'Məhsul',
                'verbose_name_plural': 'Məhsullar',
                'db_table': 'product',
            },
        ),
    ]

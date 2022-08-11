from __future__ import absolute_import, unicode_literals
import traceback
import re
import unicodedata
from product.models import MainCatalogModel, SubCatalogModel, ProductModel
from celery import shared_task
from bs4 import BeautifulSoup
import requests


@shared_task
def scapy():
    url = "https://bravomarket.online"
    r = requests.get(url=url)
    soup = BeautifulSoup(r.content, "html.parser")

    catalogLinksParent = soup.find_all("li", attrs={"class": "bx-nav-parent"})

   
    for mainCatalog in catalogLinksParent:
        # Alt kataloqlarin adi ve sehife linkleri -> List
        catalogLinks = mainCatalog.ul.find_all("li", attrs={"class": "bx-nav-2-lvl"})[
            1:
        ]

        # Esas kataloqlarin adi -> Text
        mainCatalogName = mainCatalog.a.text.strip()
        try:

            mainCatalogGet = MainCatalogModel.objects.get(name=mainCatalogName)
        except MainCatalogModel.DoesNotExist:
            mainCatalogGet = MainCatalogModel.objects.create(name=mainCatalogName)
        
        mainCatalogGet.name = mainCatalogName
        mainCatalogGet.save()
        

        for subCatalog in catalogLinks:

            # Alt kataloqun adi
            subCatalogName = subCatalog.span.text

            try:
                sub = SubCatalogModel.objects.get(name = subCatalogName)
            except SubCatalogModel.DoesNotExist:
                sub = SubCatalogModel()
            sub.name = subCatalogName
            sub.main_catalog = mainCatalogGet

            sub.save()

            # Alt kataloqun linki
            sub_catalog_link = subCatalog.a.get("href")

            # Alt kataloqlu mehsullarin sehifesi
            all_link = url + sub_catalog_link
            r2 = requests.get(url=all_link)
            soup2 = BeautifulSoup(r2.content, "html.parser")
            try:

                pages = len(
                    soup2.find_all(
                        "ul", attrs={"class": "bx_pagination_page_list_num"}
                    )[0].find_all("li")
                )

                for page in range(1, pages):
                    page_link = all_link + f"?PAGEN_1={page}"
                    r3 = requests.get(url=page_link)
                    products_soup = BeautifulSoup(r3.content, "html.parser")

                    products = products_soup.find_all(
                        "div", attrs={"class": "product_item"}
                    )

                    for product in products:
                        product_name = product.find("div", attrs={"class": "name"}).text
                        product_price = product.find(
                            "div", attrs={"class": "product-item-price-current"}
                        ).span.next.next.text.replace("₼", "")
                        p_o_p = unicodedata.normalize(
                            "NFKD",
                            product.find("div", attrs={"class": "old_price"}).span.text,
                        )
                        product_old_price = (re.subn("[₼, ]", "", p_o_p))[0]

                        try:
                            pro = ProductModel.objects.get(name=product_name)

                        except ProductModel.DoesNotExist:
                            pro = ProductModel()

                        except:
                            print(traceback.format_exc())

                        pro.name = product_name
                        pro.price = product_price
                        pro.old_price = product_old_price

                        pro.save()

                        try:

                            _sub_catalog = SubCatalogModel.objects.get(
                                name=subCatalogName
                            )
                            pro.catalog.add(_sub_catalog)
                            

                        except SubCatalogModel.DoesNotExist:
                            pass

                   
            except:

                products = soup2.find_all("div", attrs={"class": "product_item"})
                for product in products:
                    product_name = product.find("div", attrs={"class": "name"}).text
                    product_price = product.find(
                        "div", attrs={"class": "product-item-price-current"}
                    ).span.next.next.text.replace("₼", "")
                    p_o_p = unicodedata.normalize(
                        "NFKD",
                        product.find("div", attrs={"class": "old_price"}).span.text,
                    )
                    product_old_price = (re.subn("[₼, ]", "", p_o_p))[0]

                    try:
                        pro = ProductModel.objects.get(name=product_name)

                    except ProductModel.DoesNotExist:
                        pro = ProductModel()

                    pro.name = product_name
                    pro.price = product_price
                    pro.old_price = product_old_price

                    pro.save()

                    try:

                        _sub_catalog = SubCatalogModel.objects.get(name=subCatalogName)
                        pro.catalog.add(_sub_catalog)
                 

                    except SubCatalogModel.DoesNotExist:
                        pass

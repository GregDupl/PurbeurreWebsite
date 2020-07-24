"""Classes for the application purbeurre"""

from django.core.management.base import BaseCommand
import requests
from homepage.models import *

CATEGORY = {
    1: "pizzas",
    2: "biscuits",
    3: "plats-prepares",
    4: "cereales-et-derives",
    5: "surgeles",
}


class GetProduct:
    """Class to create product objects"""

    def __init__(self, data, num_product, category):
        self.code = data["products"][num_product]["code"]
        self.name = data["products"][num_product]["product_name"]
        self.keywords = data["products"][num_product]["_keywords"]
        self.brand = data["products"][num_product]["brands"]
        self.nutri = data["products"][num_product]["nutrition_grades"]
        self.fat_value = data["products"][num_product]["nutriments"]["fat_100g"]
        self.fat_level = data["products"][num_product]["nutrient_levels"]["fat"]
        self.saturated_value = data["products"][num_product]["nutriments"][
            "saturated-fat_100g"
        ]
        self.saturated_level = data["products"][num_product]["nutrient_levels"][
            "saturated-fat"
        ]
        self.salt_value = data["products"][num_product]["nutriments"]["salt"]
        self.salt_level = data["products"][num_product]["nutrient_levels"]["salt"]
        self.sugars_value = data["products"][num_product]["nutriments"]["sugars"]
        self.sugars_level = data["products"][num_product]["nutrient_levels"]["sugars"]
        self.stores = data["products"][num_product]["stores"]
        self.link = "https://fr.openfoodfacts.org/produit/" + self.code
        self.img = data["products"][num_product]["image_url"]
        self.cat = category

    def list_attributes(self):
        return (
            self.code,
            self.name,
            self.keywords,
            self.brand,
            self.nutri,
            self.fat_value,
            self.saturated_value,
            self.salt_value,
            self.sugars_value,
            self.fat_level,
            self.saturated_level,
            self.salt_level,
            self.sugars_level,
            self.stores,
            self.link,
            self.img,
            self.cat,
        )


class GetCategory:
    """Class to create category objects"""

    def __init__(self, name):
        self.name = name


class Database:
    """Insertion datas from OpenFoodFact in purbeurre's database"""

    def get_api_product(self, category_name, page_number):
        page = (
            "https://fr.openfoodfacts.org/categorie/"
            + category_name
            + "/"
            + str(page_number)
            + ".json"
        )
        r = requests.get(page)
        data = r.json()
        return data

    def insert_data(self, maximum):
        for value in CATEGORY.values():
            cat = GetCategory(value)

            if not Category.objects.filter(name=cat.name).exists():
                Category.objects.create(name=cat.name)

            key = Category.objects.get(name=cat.name)

            total_products = 0
            page_number = 1
            while total_products < maximum:
                data = self.get_api_product(cat.name, page_number)

                product_number = 0
                while (
                    product_number < len(data["products"]) and total_products < maximum
                ):
                    # verify quality of the data collected
                    # before insert it in local database
                    try:
                        product_object = GetProduct(data, product_number, key)
                        attributes = product_object.list_attributes()

                        for item in attributes:
                            assert len(str(item)) > 0
                    except KeyError:
                        pass
                    except AssertionError:
                        pass
                    else:
                        total_products += 1

                        if not Product.objects.filter(
                            code=product_object.code
                        ).exists():
                            Product.objects.create(
                                code=product_object.code,
                                name=product_object.name,
                                keywords=product_object.keywords,
                                brand=product_object.brand,
                                nutriscore=product_object.nutri,
                                fat_value=product_object.fat_value,
                                saturated_value=product_object.saturated_value,
                                salt_value=product_object.salt_value,
                                sugars_value=product_object.sugars_value,
                                fat_level=product_object.fat_level,
                                saturated_level=product_object.saturated_level,
                                salt_level=product_object.salt_level,
                                sugars_level=product_object.sugars_level,
                                stores=product_object.stores,
                                link=product_object.link,
                                image=product_object.img,
                                id_category=product_object.cat,
                            )
                    product_number += 1
                page_number += 1


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Updating database...")
        newData = Database()
        newData.insert_data(10)
        print("Done !")

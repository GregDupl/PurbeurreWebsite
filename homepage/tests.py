from homepage.models import *
from homepage.management.commands.database import *
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client
from unittest.mock import Mock


def create_temporary_datas():
    Category.objects.create(name="temp")
    Product.objects.create(
        code="temporaryProduct",
        name="temporaryProduct",
        keywords="temporaryProduct",
        brand="temporaryProduct",
        nutriscore="A",
        fat_value="temporaryProduct",
        saturated_value="temporaryProduct",
        salt_value="temporaryProduct",
        sugars_value="temporaryProduct",
        fat_level="temporaryProduct",
        saturated_level="temporaryProduct",
        salt_level="temporaryProduct",
        sugars_level="temporaryProduct",
        stores="temporaryProduct",
        link="temporaryProduct",
        image="temporaryProduct",
        id_category=Category.objects.get(name="temp"),
    )


class IndexTestCase(TestCase):
    def test_index(self):
        c = Client()
        response = c.get(reverse("homepage:index"))
        self.assertEqual(response.status_code, 200)


class legalTestCase(TestCase):
    def test_legal(self):
        c = Client()
        response = c.get(reverse("homepage:legal"))
        self.assertEqual(response.status_code, 200)


class AccountTestCase(TestCase):
    def setUp(self):
        User.objects.create_user("temporary", "temporary@mail.com", "secret")

    def test_account(self):
        c = Client()
        c.login(username="temporary", password="secret")
        response = c.get(reverse("homepage:account"))
        self.assertEqual(response.status_code, 200)


class FavorisTestCase(TestCase):
    def setUp(self):
        User.objects.create_user("temporary", "temporary@mail.com", "secret")

    def test_favoris(self):
        c = Client()
        c.login(username="temporary", password="secret")
        response = c.get(reverse("homepage:favoris"))
        self.assertEqual(response.status_code, 200)


class LogoutTestCase(TestCase):
    def setUp(self):
        User.objects.create_user("temporary", "temporary@mail.com", "secret")

    def test_logout(self):
        c = Client()
        c.login(username="temporary", password="secret")

        response = c.get(reverse("homepage:logout"))
        self.assertEqual(response.status_code, 200)


class CreateTestCase(TestCase):
    def test_create(self):
        initial_number = User.objects.count()
        c = Client()
        response = c.post(
            reverse("homepage:create"),
            {"name": "temporary", "mail": "temporary@mail.com", "password": "secret"},
        )
        new_number = User.objects.count()
        # return 200
        self.assertEqual(response.status_code, 200)
        # creation new user in database
        self.assertEqual(new_number, initial_number + 1)


class LoginTestCase(TestCase):
    def setUp(self):
        User.objects.create_user("temporary", "temporary@mail.com", "secret")

    def test_login(self):
        user = User.objects.get(username="temporary")
        c = Client()
        c.login(username="temporary", password="secret")
        response = c.post(
            reverse("homepage:login"), {"name": "temporary", "password": "secret"}
        )

        self.assertEqual(response.status_code, 200)


class SearchTestCase(TestCase):
    def test_search(self):
        c = Client()
        response = c.get(reverse("homepage:search"), {"query": "temporary"})
        self.assertEqual(response.status_code, 200)


class SubstitutTestCase(TestCase):
    def setUp(self):
        create_temporary_datas()

    def test_substitut(self):
        c = Client()
        id_product = Product.objects.get(name="temporaryProduct").id
        response = c.get(reverse("homepage:substituts", kwargs={"id": id_product}))
        self.assertEqual(response.status_code, 200)


class DetailTestCase(TestCase):
    def setUp(self):
        create_temporary_datas()

    def test_detail(self):
        c = Client()
        id_product = Product.objects.get(name="temporaryProduct").id
        response = c.get(reverse("homepage:detail", kwargs={"id": id_product}))
        self.assertEqual(response.status_code, 200)


class SaveTestCase(TestCase):
    def setUp(self):
        User.objects.create_user("temporary", "temporary@mail.com", "secret")
        create_temporary_datas()

    def test_save(self):
        initial_number = Favoris.objects.count()
        product = Product.objects.get(name="temporaryProduct")
        c = Client()
        c.login(username="temporary", password="secret")
        response = c.post(
            reverse("homepage:save"),
            {"id": product.id},
            content_type="application/json",
        )
        new_number = Favoris.objects.count()
        # return 200
        self.assertEqual(response.status_code, 200)
        # creation new favoris in database
        self.assertEqual(new_number, initial_number + 1)
        self.assertIsInstance(
            Favoris.objects.get(product_id=product).product_id, Product
        )


class DatabaseCmdTestCase(TestCase):
    def setUp(self):
        self.FAKE_DATA = {
            "products": [
                {
                    "code": "fake_code",
                    "product_name": "fake_name",
                    "_keywords": "fake_keywods",
                    "brands": "fake_brands",
                    "nutrition_grades": "A",
                    "nutriments": {
                        "fat_100g": "fake_fat",
                        "saturated-fat_100g": "fake_saturated",
                        "salt": "fake_salt",
                        "sugars": "fake_sugars",
                    },
                    "nutrient_levels": {
                        "fat": "fake_level",
                        "saturated-fat": "fake_level",
                        "salt": "fake_level",
                        "sugars": "fake_level",
                    },
                    "stores": "fake_stores",
                    "image_url": "fake_img",
                }
            ]
        }

    def test_GetProduct(self):
        fake_product = GetProduct(self.FAKE_DATA, 0, "pizzas")
        self.assertIsInstance(fake_product, GetProduct)
        self.assertEqual(fake_product.code, "fake_code")

    def test_list_attributes(self):
        fake_product = GetProduct(self.FAKE_DATA, 0, "pizzas")
        fake_tuple = fake_product.list_attributes()
        self.assertEqual(len(fake_tuple), 17)

    def test_insertInDatabase(self):
        fake_data = Database()
        fake_data.get_api_product = Mock(return_value=self.FAKE_DATA)
        response = fake_data.get_api_product()
        self.assertEqual(response["products"][0]["code"], "fake_code")

        fake_data.insert_data(1)
        self.assertIsNotNone(Product.objects.filter(name="fake_name"))


class DeleteTestCase(TestCase):
    def setUp(self):
        User.objects.create_user("temporary", "temporary@mail.com", "secret")
        create_temporary_datas()


    def test_delete(self):
        product = Product.objects.get(name="temporaryProduct")
        user = User.objects.get(username="temporary")
        favoris = Favoris.objects.create(product_id=product, user=user)
        c = Client()
        c.login(username="temporary", password="secret")

        initial_number = Favoris.objects.count()
        response = c.get(reverse("homepage:delete", kwargs={"id": product.id}))
        new_number = Favoris.objects.count()
        self.assertEqual(initial_number,new_number + 1)
        self.assertEqual(response.status_code, 200)

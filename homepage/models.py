from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)


class Product(models.Model):
    code = models.CharField(max_length=45)
    name = models.CharField(max_length=250)
    keywords = models.TextField()
    brand = models.CharField(max_length=250)
    nutriscore = models.CharField(max_length=1)
    fat_value = models.CharField(max_length=100, default='DEFAULT VALUE')
    saturated_value = models.CharField(max_length=100, default='DEFAULT VALUE')
    salt_value = models.CharField(max_length=100, default='DEFAULT VALUE')
    sugars_value = models.CharField(max_length=100, default='DEFAULT VALUE')
    fat_level = models.CharField(max_length=100, default='DEFAULT VALUE')
    saturated_level = models.CharField(max_length=100, default='DEFAULT VALUE')
    salt_level = models.CharField(max_length=100, default='DEFAULT VALUE')
    sugars_level = models.CharField(max_length=100, default='DEFAULT VALUE')
    stores = models.CharField(max_length=250)
    link = models.CharField(max_length=100)
    image = models.CharField(max_length=250, default='DEFAULT VALUE')
    id_category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Favoris(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints= [
        models.UniqueConstraint(fields=['product_id','user'], name='uniqueFavoris')
        ]

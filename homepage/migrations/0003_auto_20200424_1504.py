# Generated by Django 3.0.4 on 2020-04-24 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_auto_20200424_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='keywords',
            field=models.TextField(),
        ),
    ]

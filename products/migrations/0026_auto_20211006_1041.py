# Generated by Django 3.2.7 on 2021-10-06 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0025_offer_delivery_minimum'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sku',
        ),
        migrations.AddField(
            model_name='price',
            name='sku',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]

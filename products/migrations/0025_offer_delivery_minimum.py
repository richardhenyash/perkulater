# Generated by Django 3.2.7 on 2021-10-06 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0024_offer_delivery_percentage'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='delivery_minimum',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]

# Generated by Django 3.2.7 on 2021-11-15 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0044_alter_price_sku'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image_alt',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
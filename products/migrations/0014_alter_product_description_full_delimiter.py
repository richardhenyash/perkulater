# Generated by Django 3.2.7 on 2021-09-23 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20210923_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='description_full_delimiter',
            field=models.CharField(blank=True, max_length=3),
        ),
    ]
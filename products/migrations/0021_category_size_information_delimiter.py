# Generated by Django 3.2.7 on 2021-09-24 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_category_type_information_delimiter'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='size_information_delimiter',
            field=models.CharField(blank=True, max_length=3),
        ),
    ]
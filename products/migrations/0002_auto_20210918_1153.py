# Generated by Django 3.2.7 on 2021-09-18 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Prices',
            new_name='Price',
        ),
        migrations.RenameModel(
            old_name='Sizes',
            new_name='Size',
        ),
        migrations.RenameModel(
            old_name='Types',
            new_name='Type',
        ),
    ]

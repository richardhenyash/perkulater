# Generated by Django 3.2.7 on 2021-09-18 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_price_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coffee',
            name='name',
        ),
    ]

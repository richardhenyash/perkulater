# Generated by Django 3.2.7 on 2021-10-14 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='original_basket',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
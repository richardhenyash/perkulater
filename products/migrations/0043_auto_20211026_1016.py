# Generated by Django 3.2.7 on 2021-10-26 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0042_alter_product_description_full'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coffee',
            name='altitude',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='country',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='farm',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='flavour_profile',
            field=models.CharField(max_length=254),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='owner',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='region',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='town',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='coffee',
            name='variety',
            field=models.CharField(max_length=100),
        ),
    ]
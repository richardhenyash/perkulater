# Generated by Django 3.2.7 on 2021-10-25 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0005_order_previous_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='previous_total',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, null=True),
        ),
    ]

# Generated by Django 3.2.4 on 2021-11-14 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellerSide', '0012_cart_buyer'),
    ]

    operations = [
        migrations.AddField(
            model_name='products_post',
            name='ship_cost',
            field=models.IntegerField(default=5000),
            preserve_default=False,
        ),
    ]
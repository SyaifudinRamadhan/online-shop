# Generated by Django 3.2.4 on 2021-11-09 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellerSide', '0007_products_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='promo',
            name='active',
            field=models.CharField(default='True', max_length=10),
            preserve_default=False,
        ),
    ]

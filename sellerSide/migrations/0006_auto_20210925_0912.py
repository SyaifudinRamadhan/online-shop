# Generated by Django 3.2.7 on 2021-09-25 09:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminSide', '0001_initial'),
        ('sellerSide', '0005_promo_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promo',
            name='promo_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminSide.promo_type'),
        ),
        migrations.AlterField(
            model_name='stuff',
            name='stuff_cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminSide.category'),
        ),
        migrations.DeleteModel(
            name='category',
        ),
        migrations.DeleteModel(
            name='promo_type',
        ),
    ]
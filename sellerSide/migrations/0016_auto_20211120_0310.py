# Generated by Django 3.2.9 on 2021-11-20 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sellerSide', '0015_rating_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='stuff',
            name='dummy',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='stuff',
            name='img_file',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]

# Generated by Django 3.2.4 on 2021-11-13 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sellerSide', '0010_stuff_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('state_buy', models.CharField(max_length=15)),
                ('state_order', models.CharField(max_length=15)),
                ('count', models.IntegerField()),
                ('stuff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellerSide.stuff')),
            ],
        ),
    ]

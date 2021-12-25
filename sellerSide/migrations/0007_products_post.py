# Generated by Django 3.2.4 on 2021-11-09 03:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sellerSide', '0006_auto_20210925_0912'),
    ]

    operations = [
        migrations.CreateModel(
            name='products_post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('note', models.TextField(max_length=255)),
                ('stuff_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sellerSide.stuff')),
            ],
        ),
    ]
# Generated by Django 3.2.9 on 2021-12-13 18:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loginSys', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_sec',
            name='unique_key',
        ),
    ]

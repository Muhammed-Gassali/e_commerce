# Generated by Django 3.1.2 on 2020-11-14 00:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_auto_20201113_1201'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='category',
            new_name='category_name',
        ),
    ]

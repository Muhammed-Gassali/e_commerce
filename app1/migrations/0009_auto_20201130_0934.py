# Generated by Django 3.1.2 on 2020-11-30 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_order_order_verify'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='date_added',
            field=models.DateField(auto_now_add=True),
        ),
    ]

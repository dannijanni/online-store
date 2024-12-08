# Generated by Django 4.2.5 on 2023-09-29 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_manager', '0002_productitem_is_on_sale'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='order_manager.orderproductitem'),
        ),
        migrations.AddField(
            model_name='order',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='ordered_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
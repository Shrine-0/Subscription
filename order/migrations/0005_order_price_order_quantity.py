# Generated by Django 4.2.2 on 2023-07-04 10:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0004_order_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="price",
            field=models.DecimalField(decimal_places=2, default=1000, max_digits=10),
        ),
        migrations.AddField(
            model_name="order",
            name="quantity",
            field=models.IntegerField(default=1),
        ),
    ]

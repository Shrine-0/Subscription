# Generated by Django 4.2.2 on 2023-07-04 08:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0004_remove_product_category_alter_product_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="name",
            field=models.CharField(
                choices=[("Free", "Free"), ("Premium", "Premium")],
                default="Free",
                max_length=200,
            ),
        ),
    ]

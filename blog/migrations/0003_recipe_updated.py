# Generated by Django 4.2.7 on 2023-12-01 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_recipe_product_delete_kitchen_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]

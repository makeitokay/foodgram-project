# Generated by Django 3.1.1 on 2020-09-05 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0003_tag_display_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipeingredients",
            name="amount",
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
    ]

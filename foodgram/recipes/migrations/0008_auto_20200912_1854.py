# Generated by Django 3.1.1 on 2020-09-12 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0007_auto_20200907_0017"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tag",
            name="name",
            field=models.CharField(db_index=True, max_length=15),
        ),
    ]

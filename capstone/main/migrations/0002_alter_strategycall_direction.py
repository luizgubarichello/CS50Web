# Generated by Django 4.1 on 2022-08-25 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="strategycall",
            name="direction",
            field=models.CharField(
                choices=[("Buy", "Compra"), ("Sell", "Venda")], max_length=4
            ),
        ),
    ]

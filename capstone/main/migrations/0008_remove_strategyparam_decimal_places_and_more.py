# Generated by Django 4.1 on 2022-08-26 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_symbol_calls_prefix"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="strategyparam",
            name="decimal_places",
        ),
        migrations.AddField(
            model_name="symbol",
            name="decimal_places",
            field=models.IntegerField(default=2),
        ),
    ]

# Generated by Django 4.1 on 2022-08-26 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_remove_strategyparam_calls_denomination_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="symbol",
            name="calls_prefix",
            field=models.CharField(blank=True, default="", max_length=4),
        ),
    ]
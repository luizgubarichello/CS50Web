# Generated by Django 4.1 on 2022-08-25 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_strategycall_trade_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="strategyparam",
            name="calls_denomination",
            field=models.CharField(default="pontos", max_length=16),
        ),
    ]
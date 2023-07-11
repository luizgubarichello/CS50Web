# Generated by Django 4.0.6 on 2022-07-27 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_alter_auctionlisting_l_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='l_category',
            field=models.ForeignKey(default='Other', on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='auctions.category'),
        ),
    ]
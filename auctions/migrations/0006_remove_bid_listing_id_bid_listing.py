# Generated by Django 4.1.7 on 2023-03-23 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_rename_current_price_auctionlisting_starting_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='listing_id',
        ),
        migrations.AddField(
            model_name='bid',
            name='listing',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auctions.auctionlisting'),
            preserve_default=False,
        ),
    ]

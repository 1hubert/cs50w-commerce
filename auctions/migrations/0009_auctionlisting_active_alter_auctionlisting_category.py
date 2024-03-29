# Generated by Django 4.1.7 on 2023-03-23 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_auctionlisting_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlisting',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='category',
            field=models.CharField(choices=[('CLOTHING', 'Clothing & Accessories'), ('HEALTH', 'Health & Beauty'), ('FITNESS', 'Fitness'), ('JEWELRY', 'Jewelry'), ('PET', 'Pet Supplies'), ('MOBILE', 'Mobile Phones & Accessories'), ('CAMERAS', 'Cameras & Photos')], max_length=50),
        ),
    ]

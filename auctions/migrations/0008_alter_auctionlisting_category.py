# Generated by Django 4.1.7 on 2023-03-23 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_alter_auctionlisting_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='category',
            field=models.CharField(choices=[('Clothing & Accessories', 'Clothing & Accessories'), ('Health & Beauty', 'Health & Beauty'), ('Fitness', 'Fitness'), ('Jewelry', 'Jewelry'), ('Pet Supplies', 'Pet Supplies'), ('Mobile Phones & Accessories', 'Mobile Phones & Accessories'), ('Cameras & Photos', 'Cameras & Photos')], max_length=50),
        ),
    ]

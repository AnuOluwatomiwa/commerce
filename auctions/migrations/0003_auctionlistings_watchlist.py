# Generated by Django 5.1.4 on 2024-12-12 17:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auctionlistings_is_active_auctionlistings_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='auctionlistings',
            name='watchlist',
            field=models.ManyToManyField(blank=True, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 4.2 on 2023-05-09 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_comment_bid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bid',
            name='user',
        ),
        migrations.AlterField(
            model_name='bid',
            name='bid',
            field=models.PositiveIntegerField(),
        ),
    ]

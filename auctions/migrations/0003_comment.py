# Generated by Django 3.2.13 on 2022-06-08 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20220608_1044'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('user', models.CharField(max_length=64)),
                ('listing_id', models.IntegerField()),
            ],
        ),
    ]

# Generated by Django 2.1 on 2019-12-22 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_auto_20191222_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='is_ready',
            field=models.BooleanField(default=False),
        ),
    ]

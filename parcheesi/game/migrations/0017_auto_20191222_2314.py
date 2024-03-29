# Generated by Django 2.1 on 2019-12-22 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0016_player_artifact_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='skipLeftRound',
            new_name='cycle_count',
        ),
        migrations.AddField(
            model_name='game',
            name='cell_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='player',
            name='skip_left_round',
            field=models.IntegerField(default=0),
        ),
    ]

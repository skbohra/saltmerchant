# Generated by Django 5.0.2 on 2024-02-16 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_gamesession_game_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='player_name',
            field=models.CharField(max_length=20, unique=True),
        ),
    ]

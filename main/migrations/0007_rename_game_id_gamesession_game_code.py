# Generated by Django 5.0.2 on 2024-02-16 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_userfactory_playerfactory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gamesession',
            old_name='game_id',
            new_name='game_code',
        ),
    ]

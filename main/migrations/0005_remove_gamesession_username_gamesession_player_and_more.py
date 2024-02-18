# Generated by Django 5.0.2 on 2024-02-10 07:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_player_remove_payoutcard_payout_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamesession',
            name='username',
        ),
        migrations.AddField(
            model_name='gamesession',
            name='player',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='main.player'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='UserFactory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('automation', models.ManyToManyField(to='main.automationcard')),
                ('factory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.factorycard')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.gamesession')),
                ('labour', models.ManyToManyField(to='main.labourcard')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.player')),
                ('well', models.ManyToManyField(to='main.wellcard')),
            ],
        ),
    ]
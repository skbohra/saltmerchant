# Generated by Django 5.0.2 on 2024-02-10 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_wellcard'),
    ]

    operations = [
        migrations.AddField(
            model_name='factorycard',
            name='factory_type',
            field=models.CharField(choices=[('free_flow', 'free_flow'), ('iodized', 'iodized'), ('crude', 'crude')], default='free_flow', max_length=20),
            preserve_default=False,
        ),
    ]

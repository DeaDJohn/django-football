# Generated by Django 4.1.4 on 2022-12-30 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0009_alter_player_birth_alter_player_sing_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='birth',
            field=models.DateTimeField(max_length=300),
        ),
        migrations.AlterField(
            model_name='player',
            name='sing_date',
            field=models.DateTimeField(max_length=300),
        ),
    ]

# Generated by Django 4.1.4 on 2022-12-30 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0011_alter_player_birth_alter_player_sing_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='birth',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='player',
            name='end_contract',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='player',
            name='sing_date',
            field=models.DateField(),
        ),
    ]

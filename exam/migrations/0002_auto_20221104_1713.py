# Generated by Django 3.2.11 on 2022-11-04 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ca',
            name='live',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='exam',
            name='live',
            field=models.BooleanField(default=False),
        ),
    ]

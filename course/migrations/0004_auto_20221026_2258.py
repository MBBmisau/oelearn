# Generated by Django 3.2.11 on 2022-10-26 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_auto_20221026_1710'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='video_file',
            field=models.FileField(blank=True, null=True, upload_to='content/video'),
        ),
        migrations.AlterField(
            model_name='video',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]

# Generated by Django 3.2.11 on 2022-11-09 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='passport',
            field=models.ImageField(blank=True, null=True, upload_to='teacher'),
        ),
    ]
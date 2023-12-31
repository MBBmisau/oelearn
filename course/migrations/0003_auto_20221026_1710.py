# Generated by Django 3.2.11 on 2022-10-26 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='module',
            old_name='is_open',
            new_name='live',
        ),
        migrations.AddField(
            model_name='course',
            name='is_certificate_free',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='course',
            name='is_free',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='course',
            name='registration_open',
            field=models.BooleanField(default=True, help_text='Unless marked, students can not register this course'),
        ),
        migrations.AlterField(
            model_name='course',
            name='live',
            field=models.BooleanField(default=True, help_text='Unless marked, student can not acess this course.'),
        ),
    ]

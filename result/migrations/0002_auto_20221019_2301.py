# Generated by Django 3.2.11 on 2022-10-19 22:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0001_initial'),
        ('course', '0002_initial'),
        ('result', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentca',
            name='batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.batch'),
        ),
        migrations.AlterField(
            model_name='studentca',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course'),
        ),
        migrations.AlterField(
            model_name='studentca',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.module'),
        ),
        migrations.AlterField(
            model_name='studentexam',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course'),
        ),
        migrations.AlterField(
            model_name='studentresult',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course'),
        ),
    ]

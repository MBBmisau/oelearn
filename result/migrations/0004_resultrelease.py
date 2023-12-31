# Generated by Django 3.2.11 on 2022-11-07 08:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0002_batch_live'),
        ('result', '0003_alter_studentexam_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultRelease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('released', models.BooleanField()),
                ('created', models.DateField(auto_now_add=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academic.batch', unique=True)),
            ],
        ),
    ]

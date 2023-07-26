# Generated by Django 3.2.11 on 2023-07-24 13:42

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_auto_20221210_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='address',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='lga_of_origin',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='LGA of origin'),
        ),
        migrations.AlterField(
            model_name='student',
            name='nationality',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='passport',
            field=models.ImageField(blank=True, null=True, upload_to='student'),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='student',
            name='state_of_origin',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

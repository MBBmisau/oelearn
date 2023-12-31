# Generated by Django 3.2.11 on 2022-10-17 19:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('passport', models.ImageField(upload_to='student')),
                ('date_of_birth', models.DateField(help_text='YYYY-MM-DD', null=True)),
                ('address', models.CharField(max_length=500)),
                ('lga_of_origin', models.CharField(max_length=200, verbose_name='LGA of origin')),
                ('state_of_origin', models.CharField(max_length=200)),
                ('nationality', models.CharField(default='Nigeria', max_length=200)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user__reg_id'],
            },
        ),
    ]

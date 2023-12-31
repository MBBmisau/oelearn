# Generated by Django 3.2.11 on 2022-10-17 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('academic', '0001_initial'),
        ('student', '0001_initial'),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_id', models.CharField(max_length=250, unique=True)),
                ('plan', models.CharField(choices=[('enrollment', 'enrollment'), ('certificate', 'certificate')], max_length=100)),
                ('amount', models.PositiveIntegerField(null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('payment_method', models.CharField(blank=True, choices=[('automatic', 'Automatic'), ('manual', 'Manual')], max_length=250, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='orders', to='academic.batch')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
            options={
                'unique_together': {('student', 'course', 'plan', 'batch')},
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txn_type', models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=128, verbose_name='Type')),
                ('description', models.TextField(blank=True, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Amount')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='InvoicePaymentReferrence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.CharField(max_length=250, unique=True)),
                ('is_used', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.invoice')),
            ],
        ),
    ]

# Generated by Django 4.2.11 on 2025-03-01 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('health', '0003_alter_patient_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='counselor',
            name='bio',
        ),
        migrations.AddField(
            model_name='counselor',
            name='email',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='counselor',
            name='license_number',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='counselor',
            name='password',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

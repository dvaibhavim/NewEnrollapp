# Generated by Django 3.1.3 on 2021-04-14 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Enrollapp', '0004_userprofileinfo_sis_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='date_of_birth',
            field=models.CharField(max_length=8),
        ),
    ]

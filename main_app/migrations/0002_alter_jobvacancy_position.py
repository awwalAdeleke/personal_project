# Generated by Django 4.1 on 2022-08-29 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobvacancy',
            name='position',
            field=models.CharField(max_length=255),
        ),
    ]

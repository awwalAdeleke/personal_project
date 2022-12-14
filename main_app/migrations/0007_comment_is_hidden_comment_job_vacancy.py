# Generated by Django 4.1 on 2022-08-31 22:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_employeetype_experiencelevel_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_hidden',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='job_vacancy',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.jobvacancy'),
        ),
    ]

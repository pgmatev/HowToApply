# Generated by Django 3.2.14 on 2022-09-08 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0003_auto_20220904_2253'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='is_marked',
            field=models.BooleanField(default=False),
        ),
    ]

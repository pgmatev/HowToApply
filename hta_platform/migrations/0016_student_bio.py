# Generated by Django 3.2.14 on 2022-08-22 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hta_platform', '0015_auto_20220720_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]

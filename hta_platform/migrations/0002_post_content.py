# Generated by Django 3.2.9 on 2021-12-06 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hta_platform', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='content',
            field=models.TextField(default='This is a test'),
            preserve_default=False,
        ),
    ]

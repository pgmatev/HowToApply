# Generated by Django 3.2.14 on 2022-09-04 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hta_platform', '0018_auto_20220904_1303'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='age',
        ),
        migrations.AddField(
            model_name='student',
            name='birthday',
            field=models.DateField(default='2002-05-05'),
            preserve_default=False,
        ),
    ]
# Generated by Django 3.2.14 on 2022-07-11 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hta_platform', '0009_auto_20220310_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='university',
            name='description',
            field=models.TextField(null=True),
        ),
    ]

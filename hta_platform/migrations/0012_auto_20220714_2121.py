# Generated by Django 3.2.14 on 2022-07-14 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hta_platform', '0011_auto_20220712_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='name',
            field=models.CharField(default='Math', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='programexam',
            unique_together={('program', 'exam')},
        ),
    ]

# Generated by Django 3.2.14 on 2022-09-04 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0002_studentexam'),
        ('hta_platform', '0017_alter_studentexam_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='exams',
            field=models.ManyToManyField(through='exams.StudentExam', to='exams.Exam'),
        ),
        migrations.DeleteModel(
            name='StudentExam',
        ),
    ]

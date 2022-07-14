# Generated by Django 3.2.14 on 2022-07-14 19:57

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hta_platform', '0014_auto_20220714_2257'),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('obligatory_coef', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(3.0)])),
            ],
        ),
        migrations.CreateModel(
            name='ProgramExam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coef', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(3.0)])),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='hta_platform.exam')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.program')),
            ],
            options={
                'unique_together': {('program', 'exam')},
            },
        ),
        migrations.AddField(
            model_name='program',
            name='exams',
            field=models.ManyToManyField(through='programs.ProgramExam', to='hta_platform.Exam'),
        ),
        migrations.AddField(
            model_name='program',
            name='university',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hta_platform.university'),
        ),
    ]

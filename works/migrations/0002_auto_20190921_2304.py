# Generated by Django 2.2.5 on 2019-09-21 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('works', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='breaktimecheck',
            name='breakEndTime',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='breaktimecheck',
            name='breakStartTime',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='breaktimecheck',
            name='todayDate',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='worktimecheck',
            name='todayDate',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='worktimecheck',
            name='workEndTime',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='worktimecheck',
            name='workStartTime',
            field=models.CharField(max_length=200),
        ),
    ]

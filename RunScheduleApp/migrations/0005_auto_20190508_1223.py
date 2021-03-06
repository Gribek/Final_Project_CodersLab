# Generated by Django 2.2 on 2019-05-08 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RunScheduleApp', '0004_trainingdiary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainingdiary',
            name='comments',
            field=models.CharField(max_length=256, verbose_name='Comments'),
        ),
        migrations.AlterField(
            model_name='trainingdiary',
            name='training_distance',
            field=models.DecimalField(decimal_places=1, max_digits=3, verbose_name='Total distance'),
        ),
        migrations.AlterField(
            model_name='trainingdiary',
            name='training_info',
            field=models.CharField(max_length=128, verbose_name='Training'),
        ),
        migrations.AlterField(
            model_name='trainingdiary',
            name='training_time',
            field=models.SmallIntegerField(verbose_name='Total time'),
        ),
    ]

# Generated by Django 2.1.4 on 2018-12-17 11:49

from django.conf import settings
import django.contrib.postgres.fields.ranges
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyTraining',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
                ('description', models.TextField(null=True)),
                ('training_type', models.CharField(max_length=32)),
                ('training_distance', models.SmallIntegerField()),
                ('additional', models.CharField(max_length=32)),
                ('additional_quantity', models.CharField(max_length=32)),
                ('accomplished', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=64)),
                ('description', models.TextField(null=True)),
                ('date_range', django.contrib.postgres.fields.ranges.DateRangeField()),
                ('is_active', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='dailytraining',
            name='workout_plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='RunScheduleApp.WorkoutPlan', unique_for_date='day'),
        ),
    ]
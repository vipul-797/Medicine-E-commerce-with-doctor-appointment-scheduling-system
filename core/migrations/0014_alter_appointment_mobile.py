# Generated by Django 4.0.2 on 2022-02-15 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='mobile',
            field=models.IntegerField(default=0),
        ),
    ]

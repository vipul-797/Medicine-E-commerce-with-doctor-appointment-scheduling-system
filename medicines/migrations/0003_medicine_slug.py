# Generated by Django 3.1 on 2020-08-26 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medicines', '0002_auto_20200826_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='slug',
            field=models.SlugField(default='Fes.dmnmd<bss.d', unique=True),
        ),
    ]

# Generated by Django 2.0.7 on 2018-08-18 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postgroups', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postgroup',
            name='read_time',
        ),
    ]
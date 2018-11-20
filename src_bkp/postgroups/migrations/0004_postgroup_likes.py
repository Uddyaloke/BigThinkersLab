# Generated by Django 2.0.7 on 2018-08-23 23:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('postgroups', '0003_postgroup_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='postgroup',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='postgroup_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
# Generated by Django 2.0.7 on 2018-08-24 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='teaser',
            field=models.TextField(blank=True, max_length=50, null=True),
        ),
    ]
# Generated by Django 2.0.5 on 2018-10-09 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ua', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_phone_activated',
            field=models.BooleanField(default=False),
        ),
    ]

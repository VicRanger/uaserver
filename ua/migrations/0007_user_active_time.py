# Generated by Django 2.0.5 on 2018-12-03 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ua', '0006_auto_20181203_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='active_time',
            field=models.DateTimeField(null=True),
        ),
    ]
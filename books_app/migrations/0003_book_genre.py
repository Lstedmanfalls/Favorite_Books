# Generated by Django 2.2 on 2021-08-23 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_app', '0002_auto_20210813_0833'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
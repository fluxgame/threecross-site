# Generated by Django 3.0.6 on 2020-05-10 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20200510_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='sort_order',
            field=models.IntegerField(default=0),
        ),
    ]
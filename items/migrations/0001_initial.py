# Generated by Django 3.0.6 on 2020-07-27 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('active', models.BooleanField(default=True)),
                ('type', models.CharField(choices=[('RI', 'Raw Materials'), ('FI', 'Finished Goods'), ('ME', 'Merchandise'), ('NI', 'Non-Inventory')], default='NI', max_length=2)),
            ],
        ),
    ]

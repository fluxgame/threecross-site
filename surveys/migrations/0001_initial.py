# Generated by Django 3.0.6 on 2020-07-27 14:48

import autoslug.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('slug', autoslug.fields.AutoSlugField(editable=False, populate_from='title')),
                ('real_time_results', models.BooleanField(default=False)),
                ('max_responses', models.IntegerField(default=0)),
                ('template', models.CharField(blank=True, max_length=128, null=True)),
                ('ajax_template', models.CharField(blank=True, max_length=128, null=True)),
                ('sort_questions', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=256)),
                ('prompt', models.TextField()),
                ('required', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=0)),
                ('type', models.CharField(choices=[('YN', 'Yes/No'), ('FF', 'Freeform')], default='FF', max_length=3)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='SurveyQuestionResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SurveyResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='surveys.Survey')),
            ],
        ),
    ]

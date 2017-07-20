# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pgjson.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('data', django_pgjson.fields.JsonBField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Key',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('unique_id', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('external_id', models.CharField(max_length=100, db_index=True, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='key',
            name='project',
            field=models.ForeignKey(to='ae_reflex.Project', related_name='keys'),
        ),
        migrations.AddField(
            model_name='event',
            name='project',
            field=models.ForeignKey(to='ae_reflex.Project', related_name='events'),
        ),
        migrations.AddField(
            model_name='event',
            name='source_key',
            field=models.ForeignKey(null=True, to='ae_reflex.Key'),
        ),
    ]

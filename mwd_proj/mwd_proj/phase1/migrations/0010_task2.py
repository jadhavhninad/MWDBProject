# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phase1', '0009_auto_20170911_0751'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('genre', models.TextField(default='', null=True)),
                ('tag', models.TextField(default='', null=True)),
                ('score', models.FloatField(null=True)),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NJRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_id', models.CharField(max_length=64)),
                ('source', models.CharField(max_length=64)),
                ('dest', models.CharField(max_length=64)),
                ('time_stamp', models.DateTimeField(verbose_name=b'')),
                ('summary', models.CharField(max_length=256)),
                ('detail', models.CharField(max_length=20000)),
            ],
        ),
    ]

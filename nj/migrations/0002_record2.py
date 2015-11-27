# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nj', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record2',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event_id', models.CharField(max_length=64)),
                ('src_ip', models.CharField(max_length=16)),
                ('dst_ip', models.CharField(max_length=16)),
                ('src_port', models.CharField(max_length=6)),
                ('dst_port', models.CharField(max_length=6)),
                ('src_name', models.CharField(max_length=32)),
                ('dst_name', models.CharField(max_length=32)),
                ('time_stamp', models.DateTimeField(verbose_name=b'')),
                ('summary', models.CharField(max_length=256)),
                ('detail', models.CharField(max_length=20000)),
            ],
        ),
    ]

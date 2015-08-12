# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('console', '0002_node_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='name',
            field=models.CharField(unique=True, max_length=32),
        ),
    ]

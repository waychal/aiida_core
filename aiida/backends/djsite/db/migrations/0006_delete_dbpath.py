# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from aiida.backends.djsite.db.migrations import update_schema_version


SCHEMA_VERSION = "1.0.6"

class Migration(migrations.Migration):

    dependencies = [
        ('db', '0005_add_cmtime_indices'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dbpath',
            name='child',
        ),
        migrations.RemoveField(
            model_name='dbpath',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='dbnode',
            name='children',
        ),
        migrations.DeleteModel(
            name='DbPath',
        ),
        migrations.RunSQL("""
            DROP TRIGGER IF EXISTS autoupdate_tc ON db_dblink;
            DROP FUNCTION IF EXISTS update_tc();
        """),
        update_schema_version(SCHEMA_VERSION)

    ]
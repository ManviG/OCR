# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docfile', models.FileField(upload_to=b'documents/')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.IntegerField()),
                ('authorNames', models.IntegerField()),
                ('urls', models.IntegerField()),
                ('email', models.IntegerField()),
                ('affiliation', models.IntegerField()),
                ('references', models.IntegerField()),
                ('sections', models.IntegerField()),
                ('emailAuthMap', models.IntegerField()),
                ('figHeading', models.IntegerField()),
                ('Footnotes', models.IntegerField()),
                ('TableHeading', models.IntegerField()),
                ('citToRef', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('paperid', models.IntegerField()),
                ('userid', models.CharField(max_length=100)),
                ('user_email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='response',
            name='userdetails',
            field=models.ForeignKey(to='myapp.UserDetails'),
        ),
    ]

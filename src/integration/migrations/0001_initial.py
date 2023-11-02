# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-14 07:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SlackIntegration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_token', models.CharField(max_length=100, verbose_name='API token')),
                ('channel', models.CharField(max_length=100, verbose_name='channel')),
                ('notify_issue_create', models.BooleanField(default=True, verbose_name='notify on issue creation')),
                ('notify_issue_modify', models.BooleanField(default=True, verbose_name='notify on issue modification')),
                ('notify_comment_create', models.BooleanField(default=True, verbose_name='notify when there is a new comment')),
                ('notify_sprint_start', models.BooleanField(default=True, verbose_name='notify when a sprint is started')),
                ('notify_sprint_stop', models.BooleanField(default=True, verbose_name='notify when when a sprint is stopped')),
            ],
            options={
                'verbose_name': 'slackintegration',
                'verbose_name_plural': 'slackintegrations',
            },
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-14 07:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import search.fieldcheckings


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_text', models.CharField(max_length=32, verbose_name='text')),
                ('color', models.CharField(blank=True, choices=[('e91e63', 'pink'), ('f44336', 'red'), ('9c27b0', 'purple'), ('673ab7', 'deep purple'), ('3f51b5', 'indigo'), ('2196f3', 'blue'), ('03a9f4', 'light blue'), ('00bcd4', 'cyan'), ('009688', 'teal'), ('4caf50', 'green'), ('8bc34a', 'light green'), ('cddc39', 'lime'), ('ffeb3b', 'yellow'), ('ffc107', 'amber'), ('ff9800', 'orange'), ('ff5722', 'deep orange'), ('795548', 'brown'), ('9e9e9e', 'grey'), ('607d8b', 'blue grey')], max_length=32, verbose_name='color')),
                ('font_color', models.CharField(default='fff', editable=False, max_length=32, verbose_name='font color')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='project.Project', verbose_name='project')),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
                'ordering': ('tag_text',),
            },
            bases=(search.fieldcheckings.SearchableMixin, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='tag',
            unique_together=set([('project', 'tag_text')]),
        ),
    ]

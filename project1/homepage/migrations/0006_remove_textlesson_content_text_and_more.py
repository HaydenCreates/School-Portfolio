# Generated by Django 4.2.4 on 2023-10-15 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0005_remove_textlesson_submitted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='textlesson',
            name='content_text',
        ),
        migrations.RemoveField(
            model_name='textlesson',
            name='description',
        ),
    ]

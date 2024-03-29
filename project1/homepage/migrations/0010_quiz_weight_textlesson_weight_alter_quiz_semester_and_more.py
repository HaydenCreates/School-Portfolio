# Generated by Django 4.2.4 on 2023-11-21 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0009_quiz_semester_textlesson_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='weight',
            field=models.FloatField(default=1.0),
        ),
        migrations.AddField(
            model_name='textlesson',
            name='weight',
            field=models.FloatField(default=1.0),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='semester',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='textlesson',
            name='semester',
            field=models.IntegerField(null=True),
        ),
    ]

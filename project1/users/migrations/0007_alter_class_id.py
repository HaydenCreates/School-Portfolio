# Generated by Django 4.2.4 on 2023-10-10 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_profile_enrolled_classes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]

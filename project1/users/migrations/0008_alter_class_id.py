# Generated by Django 4.2.4 on 2023-10-15 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_class_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]

# Generated by Django 4.2.5 on 2023-09-27 03:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classNum', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='classNum',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.class'),
        ),
    ]

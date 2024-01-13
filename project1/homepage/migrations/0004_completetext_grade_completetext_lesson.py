# Generated by Django 4.2.4 on 2023-10-08 22:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0003_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='completetext',
            name='grade',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='completetext',
            name='lesson',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='homepage.textlesson'),
        ),
    ]

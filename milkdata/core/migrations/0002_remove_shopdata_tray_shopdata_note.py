# Generated by Django 5.0.2 on 2024-02-15 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopdata',
            name='tray',
        ),
        migrations.AddField(
            model_name='shopdata',
            name='note',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

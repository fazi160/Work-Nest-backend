# Generated by Django 4.2.7 on 2023-11-15 19:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0003_alter_conferencehall_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='conferencehall',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='coworkspace',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

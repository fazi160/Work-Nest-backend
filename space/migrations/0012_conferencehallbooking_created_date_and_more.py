# Generated by Django 4.2.6 on 2023-12-07 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0011_coworkspacebooking'),
    ]

    operations = [
        migrations.AddField(
            model_name='conferencehallbooking',
            name='created_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='coworkspacebooking',
            name='created_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]

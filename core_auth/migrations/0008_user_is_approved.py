# Generated by Django 4.2.7 on 2023-11-02 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_auth', '0007_alter_customerdetail_contact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]

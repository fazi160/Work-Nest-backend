# Generated by Django 4.2.6 on 2023-12-04 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0008_delete_websocketmessage_alter_coworkspace_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conferencehall',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]

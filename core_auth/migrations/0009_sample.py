# Generated by Django 4.2.6 on 2023-11-23 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_auth', '0008_user_is_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='sample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(verbose_name=1)),
            ],
        ),
    ]

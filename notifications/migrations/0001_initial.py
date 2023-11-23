# Generated by Django 4.2.6 on 2023-11-23 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminNotificationCreate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=300)),
                ('is_opened', models.BooleanField(default=False)),
                ('notification_type', models.CharField(choices=[('register', 'register'), ('cospace', 'cospace'), ('conference', 'conference')], default='space', max_length=20)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('key', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]

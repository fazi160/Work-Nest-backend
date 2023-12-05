# Generated by Django 4.2.6 on 2023-12-02 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0006_conferencehallbooking_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebSocketMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_type', models.CharField(max_length=255)),
                ('message_data', models.JSONField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
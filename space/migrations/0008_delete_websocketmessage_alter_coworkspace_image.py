# Generated by Django 4.2.6 on 2023-12-04 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('space', '0007_websocketmessage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WebSocketMessage',
        ),
        migrations.AlterField(
            model_name='coworkspace',
            name='image',
            field=models.ImageField(upload_to='images/space/cowork'),
        ),
    ]
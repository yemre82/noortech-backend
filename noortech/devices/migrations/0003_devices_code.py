# Generated by Django 4.1.4 on 2022-12-12 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_devices'),
    ]

    operations = [
        migrations.AddField(
            model_name='devices',
            name='code',
            field=models.ImageField(blank=True, upload_to='code'),
        ),
    ]

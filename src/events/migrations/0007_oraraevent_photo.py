# Generated by Django 2.0.2 on 2018-10-28 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_eventinvites'),
    ]

    operations = [
        migrations.AddField(
            model_name='oraraevent',
            name='photo',
            field=models.ImageField(blank=True, upload_to='events', verbose_name='Event Photo'),
        ),
    ]

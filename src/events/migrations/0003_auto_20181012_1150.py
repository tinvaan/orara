# Generated by Django 2.0.2 on 2018-10-12 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20181012_1104'),
    ]

    operations = [
        migrations.RenameField(
            model_name='oraraevent',
            old_name='venue_city',
            new_name='venue_area',
        ),
        migrations.AlterField(
            model_name='oraraevent',
            name='venue_lat',
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='oraraevent',
            name='venue_lon',
            field=models.DecimalField(decimal_places=6, default=0.0, max_digits=9),
        ),
    ]

# Generated by Django 2.0.2 on 2018-11-07 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0011_auto_20181019_0646'),
    ]

    operations = [
        migrations.AddField(
            model_name='orarauser',
            name='college',
            field=models.CharField(blank=True, default='NA', max_length=80, verbose_name='College'),
        ),
        migrations.AddField(
            model_name='orarauser',
            name='workplace',
            field=models.CharField(blank=True, default='NA', max_length=60, verbose_name='Workplace'),
        ),
    ]

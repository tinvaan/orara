# Generated by Django 2.0.2 on 2018-10-11 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='socialprofiles',
            options={'verbose_name': 'Social profiles', 'verbose_name_plural': 'Social profiles'},
        ),
        migrations.AlterModelOptions(
            name='userinterests',
            options={'verbose_name': 'Interests', 'verbose_name_plural': 'Interests'},
        ),
        migrations.RenameField(
            model_name='userinterests',
            old_name='tags',
            new_name='interests',
        ),
    ]

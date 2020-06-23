# Generated by Django 2.2.5 on 2020-05-28 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegeapp', '0007_auto_20200524_1314'),
    ]

    operations = [
        migrations.RenameField(
            model_name='college',
            old_name='name',
            new_name='collegename',
        ),
        migrations.RenameField(
            model_name='course',
            old_name='name',
            new_name='coursename',
        ),
        migrations.RemoveField(
            model_name='college',
            name='locate',
        ),
        migrations.RemoveField(
            model_name='location',
            name='lname',
        ),
        migrations.AddField(
            model_name='college',
            name='Email',
            field=models.CharField(default='xyz@gmail.com', max_length=120),
        ),
        migrations.AddField(
            model_name='college',
            name='Website',
            field=models.CharField(default='google.comm', max_length=120),
        ),
        migrations.AddField(
            model_name='college',
            name='address',
            field=models.CharField(default='not specified', max_length=120),
        ),
        migrations.AddField(
            model_name='location',
            name='locationname',
            field=models.CharField(default='Others', max_length=120, verbose_name='Location Name'),
        ),
    ]

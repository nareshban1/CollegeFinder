# Generated by Django 2.2.5 on 2020-05-22 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collegeapp', '0005_auto_20200522_1112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='lname',
            field=models.CharField(default='Nepal', max_length=120, verbose_name='Location Name'),
        ),
    ]

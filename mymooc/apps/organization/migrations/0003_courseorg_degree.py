# Generated by Django 2.0 on 2018-04-30 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20180423_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='degree',
            field=models.CharField(default='全国知名', max_length=20, verbose_name='名誉'),
        ),
    ]
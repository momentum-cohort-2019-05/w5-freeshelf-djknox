# Generated by Django 2.2.2 on 2019-07-01 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0010_auto_20190627_1747'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name_plural': 'categories'},
        ),
    ]
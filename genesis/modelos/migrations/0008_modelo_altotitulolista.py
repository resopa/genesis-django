# Generated by Django 2.1.3 on 2018-12-02 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelos', '0007_auto_20181201_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelo',
            name='altotitulolista',
            field=models.SmallIntegerField(default=100),
        ),
    ]

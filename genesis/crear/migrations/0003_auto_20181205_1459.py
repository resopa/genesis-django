# Generated by Django 2.1.3 on 2018-12-05 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crear', '0002_crear_ide'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crear',
            old_name='ide',
            new_name='aplicacionid',
        ),
        migrations.AddField(
            model_name='crear',
            name='modeloid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='crear',
            name='propiedadid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='crear',
            name='proyectoid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='crear',
            name='reglaid',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]

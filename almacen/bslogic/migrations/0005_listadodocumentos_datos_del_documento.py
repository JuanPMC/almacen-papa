# Generated by Django 4.2.16 on 2025-02-27 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bslogic', '0004_actuacion_empresa_almacen_empresa_empresa_empleados_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listadodocumentos',
            name='datos_del_documento',
            field=models.FileField(default=None, upload_to='uploads/'),
            preserve_default=False,
        ),
    ]

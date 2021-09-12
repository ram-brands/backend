# Generated by Django 3.2.5 on 2021-09-12 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0003_run_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='run',
            name='input_path',
        ),
        migrations.RemoveField(
            model_name='run',
            name='output_path',
        ),
        migrations.AddField(
            model_name='run',
            name='base_path',
            field=models.CharField(default=None, max_length=200, unique=True),
            preserve_default=False,
        ),
    ]

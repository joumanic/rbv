# Generated by Django 4.2.7 on 2025-01-14 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_radioshow_show_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radioshow',
            name='show_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]

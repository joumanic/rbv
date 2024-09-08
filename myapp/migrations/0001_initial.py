# Generated by Django 5.1.1 on 2024-09-08 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RadioShow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host_name', models.CharField(max_length=255)),
                ('show_name', models.CharField(max_length=255)),
                ('genre_1', models.CharField(max_length=100)),
                ('genre_2', models.CharField(blank=True, max_length=100, null=True)),
                ('genre_3', models.CharField(blank=True, max_length=100, null=True)),
                ('show_image', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
# Generated by Django 4.1.10 on 2023-08-25 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmRestFullAPI', '0009_roomcondition_light_intensity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Automation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('maximum_temperature', models.CharField(blank=True, default='', max_length=255)),
                ('minimum_soilmoisture', models.CharField(blank=True, default='', max_length=255)),
                ('minimum_light_intensity', models.CharField(blank=True, default='', max_length=255)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]

# Generated by Django 4.1.10 on 2023-08-25 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("farmRestFullAPI", "0008_roomcondition"),
    ]

    operations = [
        migrations.AddField(
            model_name="roomcondition",
            name="light_intensity",
            field=models.CharField(blank=True, default="", max_length=255),
        ),
    ]
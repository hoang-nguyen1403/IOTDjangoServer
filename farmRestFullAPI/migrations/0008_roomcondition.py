# Generated by Django 4.1.10 on 2023-08-09 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("farmRestFullAPI", "0007_profile_about_you"),
    ]

    operations = [
        migrations.CreateModel(
            name="RoomCondition",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "temperature",
                    models.CharField(blank=True, default="", max_length=255),
                ),
                ("humidity", models.CharField(blank=True, default="", max_length=255)),
                (
                    "soilmoisture",
                    models.CharField(blank=True, default="", max_length=255),
                ),
            ],
            options={"ordering": ["-created"],},
        ),
    ]

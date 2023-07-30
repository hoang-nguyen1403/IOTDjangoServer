from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Employee(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="UserTest")
    userName = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    dob = models.DateTimeField(auto_now=True)
    email = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.userName


class ControlPanel(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="control_panel")
    created = models.DateTimeField(auto_now_add=True)
    hasFan = models.BooleanField()
    hasPump = models.BooleanField()
    hasLed = models.BooleanField()

    class Meta:
        ordering = ['-created']

    # def __str__(self):
    #     return self.created
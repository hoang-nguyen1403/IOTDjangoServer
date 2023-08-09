from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.conf import settings


class Profile(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userprofile")
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    about_you = models.CharField(max_length=255, blank=True, default='')
    def __str__(self):
        return f'Profile of {self.user.username}'


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

class RoomCondition(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    temperature = models.CharField(max_length=255, blank=True, default='')
    humidity = models.CharField(max_length=255, blank=True, default='')
    soilmoisture = models.CharField(max_length=255, blank=True, default='')

    class Meta:
        ordering = ['-created']
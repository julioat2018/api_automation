from django.db import models

from phone_field import PhoneField


class User(models.Model):
    name = models.CharField(max_length=60)
    surname = models.CharField(max_length=60)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    email = models.EmailField(max_length=40)

    def __str__(self):
        return self.name

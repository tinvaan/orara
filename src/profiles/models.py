import os

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser

from geopy import geocoders
from geopy.exc import GeocoderServiceError
from multiselectfield import MultiSelectField


INTERESTS = (
    ("NA", "RANDOM"),
    ("SP", "SPORTS"),
    ("OD", "OUTDOOR"),
    ("BK", "BOOKS"),
    ("MV", "MOVIES"),
    ("PH", "PHOTOGRAPHY"))


class OraraUser(AbstractUser):
    bio = models.CharField(verbose_name="Short Description", blank=True, max_length=240, default='None')
    photo = models.ImageField(verbose_name="Profile photo", blank=True, upload_to='profiles')
    validator = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                               message="Format(15 digits): '+999999999'.")
    phone = models.CharField(verbose_name="Contact Number", validators=[validator], max_length=17, blank=True)
    area = models.CharField(verbose_name="Area", max_length=40, blank=True)
    area_lat = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    area_lon = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.get_username()

    def save(self, *args, **kwargs):
        # Encrypt password if not encrypted
        if len(self.password.split('$')) != 4:
            self.set_password(self.password)

        # Update coordinates of user's location if not provided
        if self.area_lat == 0.0 and self.area_lon == 0.0:
            try:
                mapbox = geocoders.MapBox(api_key=os.environ.get('MAPBOX_ACCESS_TOKEN'))
                coordinates = mapbox.geocode(self.area)
                self.area_lat = coordinates.latitude
                self.area_lon = coordinates.longitude
            except (KeyError, GeocoderServiceError):
                pass

        super().save(*args, **kwargs)


class UserInterests(models.Model):
    user = models.ForeignKey(OraraUser, on_delete=models.CASCADE)
    interests = MultiSelectField(choices=INTERESTS, max_choices=3, default="NA")

    class Meta:
        verbose_name = "Interests"
        verbose_name_plural = "Interests"

    def __str__(self):
        return "Registered interests for '{}'".format(self.user)


class SocialProfiles(models.Model):
    user = models.ForeignKey(OraraUser, on_delete=models.CASCADE)
    blog = models.CharField(verbose_name="Blog", blank=True, max_length=60, default="#")
    twitter = models.CharField(verbose_name="Twitter", blank=True, max_length=40, default="#")
    linkedin = models.CharField(verbose_name="LinkedIn", blank=True, max_length=40, default="#")
    facebook = models.CharField(verbose_name="Facebook", blank=True, max_length=40, default='#')
    instagram =  models.CharField(verbose_name="Instagram", blank=True, max_length=40, default="#")
    portfolio = models.CharField(verbose_name="Portfolio", blank=True, max_length=40, default="#")

    class Meta:
        verbose_name = "Social profiles"
        verbose_name_plural = "Social profiles"

    def __str__(self):
        return "Social profile for '{}'".format(self.user)
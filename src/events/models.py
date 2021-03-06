import os

from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

from geopy import geocoders
from geopy.exc import GeocoderServiceError
from taggit.managers import TaggableManager
from multiselectfield import MultiSelectField

from profiles.models import OraraUser


EVENT_CATEGORIES = (
    ("NA", "RANDOM"),
    ("SP", "SPORTS"),
    ("OD", "OUTDOOR"),
    ("BK", "BOOKS"),
    ("MV", "MOVIES"),
    ("PH", "PHOTOGRAPHY"),
    ("DT", "DATING"),
    ("NL", "NIGHTLIFE"),
    ("TH", "TECHNICAL"),
    ("UN", "UNCATEGORIZED"))


class OraraEvent(models.Model):
    name = models.CharField(verbose_name="Event Name", blank=False, max_length=40, default="NA")
    description = models.TextField(verbose_name="Event Description", blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    venue = models.CharField(blank=False, max_length=40, default="NA")
    venue_area = models.CharField(blank=True, max_length=40)
    venue_lat = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    venue_lon = models.DecimalField(max_digits=9, decimal_places=6, default=0.0)
    website = models.CharField(blank=True, max_length=40, default="#")
    email = models.EmailField()
    validator = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                               message="Format(15 digits): '+999999999'.")
    phone = models.CharField(verbose_name="Contact", validators=[validator],
                             max_length=17, blank=True)
    image = models.ImageField(verbose_name="Event Image", blank=True, upload_to='events')
    tags = TaggableManager()
    categories = MultiSelectField(choices=EVENT_CATEGORIES, default="UN")

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.venue_lat == 0.0 and self.venue_lon == 0.0:
            try:
                mapbox = geocoders.MapBox(api_key=os.environ.get('MAPBOX_ACCESS_TOKEN'))
                coordinates = mapbox.geocode(self.venue_area)
                self.venue_lat = coordinates.latitude
                self.venue_lon = coordinates.longitude
            except (KeyError, GeocoderServiceError):
                pass

        super().save(*args, **kwargs)


class EventLikes(models.Model):
    '''
    Events liked by a user
    '''
    user = models.ForeignKey(OraraUser, on_delete=models.CASCADE)
    event = models.ForeignKey(OraraEvent, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Interested"
        verbose_name_plural = "Interested"

    def __str__(self):
        return "'{}' - '{}".format(self.event, self.user)


class EventCustomers(models.Model):
    '''
    Customers going to an event
    '''
    event = models.ForeignKey(OraraEvent, on_delete=models.CASCADE)
    customer = models.ForeignKey(OraraUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return "'{}' -- '{}'".format(self.event, self.customer)


class EventInvites(models.Model):
    event = models.ForeignKey(OraraEvent, on_delete=models.CASCADE)
    user = models.ForeignKey(OraraUser, related_name='user', on_delete=models.CASCADE)
    host = models.ForeignKey(OraraUser, related_name='host', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Invites"
        verbose_name_plural = "Invites"

    def __str__(self):
        return "'{}' invited to '{}' by '{}'".format(self.user, self.event, self.host)

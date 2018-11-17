import os
from geopy import geocoders
from geopy.exc import GeocoderServiceError

from events.external.sources.insider import get_events
from events.external.sources.meetup import upcoming_events


def mapcoordinates(city):
    try:
        mapbox = geocoders.MapBox(api_key=os.environ.get('MAPBOX_ACCESS_TOKEN'))
        coordinates = mapbox.geocode(city)
    except (KeyError, GeocoderServiceError):
        return []
    return coordinates.latitude, coordinates.longitude


def insider(city=None, tags=None):
    return get_events(city, tags)


def meetup(lat, lon):
    return upcoming_events(lat, lon)


def all(city, tags=None):
    events = []
    [events.append(e) for e in get_events(city, tags)]
    [events.append(e) for e in upcoming_events(mapcoordinates(city)[0],
                                               mapcoordinates(city)[1])]
    return events

import json
import requests


API_URL = "http://staging.api.insider.in/"


def get_carousel_event(data, city=None, tags=None):
    try:
        events = []
        for item in data['carousel']:
            for event in item['events']:
                venues = []
                for venue in event['venues']:
                    shows = []
                    for show in venue['shows']:
                        shows.append({'timestamp': show['date_string']})
                    venues.append({
                        'name': venue['name'],
                        'date': venue['date_string'],
                        'shows': shows
                    })
                events.append({
                    'name': event['name'],
                    'price': event['price_display_string'],
                    'image': event['horizontal_cover_image'],
                    'venues': venues,
                })
    except KeyError as err:
        print("Exception - 'get_carousel_image()' : ", err)
    return events


def get_featured_events(data, city=None, tags=None):
    events = []
    for index, event in enumerate(data['featured']):
        try:
            _event = {}
            _event['name'] = event['name']
            _event['image'] = event['horizontal_cover_image']
            _event['location'] = event['map_id']
            _event['description'] = event['description']
        except KeyError as err:
            print(index, "\tException - 'get_featured_events()' : ", err)
        events.append(_event)
    return events


def get_listed_events(data, city=None, tags=None):
    try:
        events = []
        for item in data['list']:
            for event in item['events']:
                venues = []
                for venue in event['venues']:
                    shows = []
                    for show in venue['shows']:
                        shows.append({'timestamp': show['date_string']})
                    venues.append({
                        'name': venue['name'],
                        'shows': shows
                    })
                events.append({
                    'name': event['name'],
                    'city': event['city'],
                    'price': event['price_display_string'],
                    'image': event['horizontal_cover_image'],
                    'venues': venues
                })
    except KeyError as err:
        print("Exception - 'get_listed_events()' : ", err)

    return events


def get_events(city=None, tags=None):
    events = []
    url = API_URL + "tag/list"
    if city:
        params = {'model': 'event', 'tags': city}
        response = requests.get(url, params)
    else:
        response = requests.get(url)

    try:
        if response.ok:
            events.extend(get_carousel_event(json.loads(response.text)['data']))
            events.extend(get_featured_events(json.loads(response.text)['data']))
            events.extend(get_listed_events(json.loads(response.text)['data']))
        else:
            print("Failed to fetch events from insider API : ", response.text)
    except KeyError as err:
        print("Exception - 'get_events()' : ", err)

    return events


if __name__ == "__main__":
    events = get_events()
    print(json.dumps(events, indent=4))

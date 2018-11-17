import os
import json
import requests


API_URL = "http://api.meetup.com/"


def get_event_photos(event):
    event_id = event['id']
    urlname = event['group']['urlname']
    params = {'photo-host': 'secure'}
    url = API_URL + "/" + urlname + "/events/" + event_id + "/photos"
    response = requests.get(url, params)

    if response.ok:
        photos = json.loads(response.text)
        return photos['highres_link']
    return "#"


def upcoming_events(lat, lon):
    url = API_URL + "find/upcoming_events"
    params = {
        "Authorization": "Bearer {}".format(os.environ.get("MEETUP_API_KEY")),
        'photo-host': 'secure',
        'lat': lat, 'lon': lon
    }
    print(params)
    response = requests.get(url, params)

    events = []
    if response.ok:
        data = json.loads(response.text)['events']
        for event in data:
            event['photos'] = get_event_photos(event)
            events.append(event)
    print(response.text)
    return events


if __name__ == "__main__":
    events = upcoming_events("18.52361", "73.84778")
    print(json.dumps(events, indent=4))
# Orara

A minimalsitic social network that helps you find;
- What's happening around you ?
- What are people around you upto ?

# Notes
What are the questions that we need to ask users ?
1. Do you want to learn more about an event happening around you, based on your interest ?
2. Do people want to connect with new people over an event or activity ? If yes:
    -- Before
    -- During
    -- After

## How to run ?

1. Install `Python3.x`(`3.6 +`, preferably) and it's corresponding package manager - `pip`
2. Configure a virtual environment for project
```
$ sudo -H pip install virtualenv
$ sudo -H pip install virtualenvwrapper

$ mkvirtualenv orara
$ workon orara
```
3. Install dependencies
```
$ pip install -r requirements.txt
```
4. Apply/update Django migrations
```
$ python src/manage.py makemigrations
$ python src/manage.py migrate
```
5. Run the server
```
$ python src/manage.py runserver
```

The server should be up and running at `http://127.0.0.1/8000`.
Navigate to `http://127.0.0.1/8000/events` or `http://127.0.0.1/8000/flocks/explore` to view some raw data.
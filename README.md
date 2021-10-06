# shorter is better

**"shorter is better"** is a project to short your urls.

## endpoints

* /auth
    - /login
    - /register


* /shortener (also /r)
    - POST: /{url} to short a link
    - GET: /{short_slug} to get original link


* /report
    - /get

## Technologies

* fastapi
* kafka
* postgresql
* redis

## USAGE
`pip install requirements.txt`
### prerequisites:
* run redis-server
* run apache kafka

`python app.py`

`python kafka_worker.py`

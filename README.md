# mozschema-validator

A continuous integration service for Mozilla pipeline schemas.

# Running

```bash
docker-compose up

curl localhost:8000/
```

# API

```
GET /v1/schemas/{id}
GET /v1/schemas
PUT /v1/validate?ids={ids}
GET /v1/summarize?id={id}
```

# Resources

* [Dockerflow](https://github.com/mozilla-services/Dockerflow)
* [Flask quickstart](http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application)
* [Docker Compose](https://docs.docker.com/compose/gettingstarted/#step-1-setup)
* [Using Celery with Flask](https://blog.miguelgrinberg.com/post/using-celery-with-flask)

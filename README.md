# mozschema-validator

A continuous integration service for Mozilla pipeline schemas.

# Usage

```bash
# build the docker components
make build

# bring up the services, this can be put into the background
make up

# in a separate shell, open the entry-point into the service
curl localhost:8000
# or through a browser
xdg-open http://localhost:8000


# bring down the service
make clean
```

## Running tests

There are currently three levels of testing in this project. The first two tests are located
within the `validator` sub-project as standard `pytest` unit and integration test. At the root
of the project, a micro-service integration test is available.

```bash
make test

# or without make
./run-compose-test.sh
```

# Architecture

The bulk schema validator is separated into two separate systems. The primary subsystem is the
pyspark application that validates a set of json documents against a schema and renders a human
readable summary. A secondary REST api provides a layer suitable for CI tooling.

Flask provides the frontend to the service. The PySpark application can be run on-demand with an
included standalone Spark docker image. Celery provides the internal task inter-op between Flask
and Spark.

The service is exposed through the REST api using a Dockerflow compatible configuration.

# Roadmap

The following features are planned for the v0 release.

* Request document-set validation through a REST api
* Support for manually mounted data volumes using the `file://` protocol
* Dockerflow compatible

The following features are planned for the v1 release.

* REST interface into the `mozilla-pipeline-schemas` repository
* Support for maria/postgres using the `jdbc://` protocol
* Interface into task queue and historical task runs

# Resources

* [Dockerflow](https://github.com/mozilla-services/Dockerflow)
* [Flask quickstart](http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application)
* [Docker Compose](https://docs.docker.com/compose/gettingstarted/#step-1-setup)
* [Using Celery with Flask](https://blog.miguelgrinberg.com/post/using-celery-with-flask)
* [Spark Standalone](https://spark.apache.org/docs/latest/spark-standalone.html)
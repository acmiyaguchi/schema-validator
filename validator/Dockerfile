FROM gettyimages/spark:latest
MAINTAINER Anthony Miyaguchi <amiyaguchi@mozilla.com>

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pip install pipenv && \
    pipenv install --system --deploy

WORKDIR /app
COPY . /app

CMD ["bin/bootstrap.sh"]
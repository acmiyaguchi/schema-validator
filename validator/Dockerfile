FROM gettyimages/spark:latest
MAINTAINER Anthony Miyaguchi <amiyaguchi@mozilla.com>

RUN pip install pipenv

WORKDIR /app
COPY . /app

RUN pipenv install --system --deploy

CMD ["bin/bootstrap.sh"]
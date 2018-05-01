FROM python:3.4.2-slim
MAINTAINER Anthony Miyaguchi <amiyaguchi@mozilla.com>

ENV PYTHONUNBUFFERED=1 \
    PORT=8000

EXPOSE $PORT

# TODO: because of local file directory permissions with spark, this user is not active
RUN groupadd --gid 10001 app && \
    useradd --gid app --uid 10001 --home-dir /app app

# application needs access to `spark-submit`
# RUN mkdir /usr/share/man/man1/
RUN echo "deb http://ftp.debian.org/debian jessie-backports main" >> /etc/apt/sources.list
RUN apt update && \
    apt install --yes -t jessie-backports openjdk-8-jre-headless ca-certificates-java

RUN apt install -y pandoc
RUN pip install --upgrade pip
RUN pip install pipenv

WORKDIR /app
COPY . /app

RUN pipenv install --system --deploy

# install dependencies for spark-submit in client mode
RUN cd validator && pipenv install --system --deploy

CMD ["python", "run.py"]
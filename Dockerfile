FROM python:3.4.2-slim
MAINTAINER Anthony Miyaguchi <amiyaguchi@mozilla.com>

# Start system bootstrap
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

EXPOSE $PORT

# Dependency of: spark-submit
RUN echo "deb http://ftp.debian.org/debian jessie-backports main" >> /etc/apt/sources.list
RUN apt update && \
    apt install --yes -t jessie-backports openjdk-8-jre-headless ca-certificates-java

# Dependency of: sphinx (used for documentation generation)
RUN apt install -y pandoc

# Dependency of: pipenv (requires more recent version than the image)
RUN pip install --upgrade pip

# Create the application user and home directory
WORKDIR /app
RUN groupadd --gid 10001 app && \
    useradd --gid app --uid 10001 --home-dir /app app
RUN chown -R app:app /app

# Make a source copy and start userland
USER app

ENV PATH=${PATH}:/app/.local/bin
RUN pip install --user pipenv

# TODO: pyenv
# Install service and application dependencies
WORKDIR /tmp/bootstrap-pip

COPY Pipfile Pipfile.lock ./
RUN pipenv sync --dev --three

# COPY ./validator/Pipfile Pipfile
# COPY ./validator/Pipfile.lock Pipfile.lock
# RUN pipenv update --dev --three

COPY . /app

# check for changes in the service .lockfile
RUN pipenv update --dev

# check for changes in the application spark-master
RUN cd validator && pipenv update --dev

CMD ["python", "run.py"]

# Hostname generator microservice

# Base image
FROM python:3

LABEL vendor="sunrize"
LABEL description="Image for hostname generation using REST"
LABEL hostname_server.release-date="2024-06-15"
LABEL hostname_server.version="0.0.0"

ENV HOSTNAME_SERVER_DATA_DIRECTORY='/data'
ENV HOSTNAME_SERVER_LISTEN_IP='0.0.0.0'
ENV HOSTNAME_SERVER_LISTEN_PORT='5000'

# Add author
LABEL org.opencontainers.image.authors="sunrize"

WORKDIR /usr/src/app

# Copy requirements for this image
COPY requirements.txt /usr/src/app

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install -r requirements.txt

# Copy app sources
COPY pyproject.toml /usr/src/app
COPY MANIFEST.in /usr/src/app
COPY docker-entrypoint.sh /usr/src/app
RUN chmod u+x ./docker-entrypoint.sh
COPY manage.py /usr/src/app
RUN chmod u+x ./manage.py
ADD hostname_server /usr/src/app/hostname_server

# Install app package
#RUN pip install --no-cache-dir -e .
RUN pip install -e .

# Make data directory
RUN mkdir /data

# Predefined port
# can be overwritten with `docker run -p ...`
EXPOSE 5000/tcp

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /usr/src/app
RUN chown -R appuser /data
USER appuser

# Run command
# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD [ "gunicorn", "-w", "1", "--bind", "0.0.0.0:5000", "hostname_server.app:app" ]
ENTRYPOINT ["./docker-entrypoint.sh"]


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
#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

# Copy app sources
ADD src /usr/src/app
COPY pyproject.toml /usr/src/app
COPY MANIFEST.in /usr/src/app
COPY LICENSE /usr/src/app
COPY docker-entrypoint.sh /usr/src/app
RUN chmod u+x ./docker-entrypoint.sh
COPY manage.py /usr/src/app
RUN chmod u+x ./manage.py

# Install app package
#RUN pip install --no-cache-dir -e .
RUN pip install -e .

# Make data directory
RUN mkdir /data

# Predefined port
# can be overwritten with `docker run -p ...`
EXPOSE 5000/tcp

# Run command
# CMD [ "gunicorn", "-w", "1", "--bind", "0.0.0.0:5000", "hostname_server.app:app" ]
ENTRYPOINT ["./docker-entrypoint.sh"]


FROM python:3-bullseye as app

# Will create externally.
VOLUME /root/.cache/pip
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

RUN adduser appuser
COPY --chown=appuser:appuser docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh

# Run as lower-permissioned user to help avoid security issues.
RUN chown -R appuser /app
USER appuser

ENTRYPOINT /usr/local/bin/docker-entrypoint.sh


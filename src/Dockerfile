FROM python:3.11-slim-bookworm

# Add application user
RUN adduser \
  --home "/opt/gthnk" \
  --uid 1000 \
  --disabled-password \
  "gthnk"

RUN python3 -m venv /opt/gthnk/.venv

RUN mkdir /usr/local/src/gthnk
COPY gthnk /usr/local/src/gthnk/gthnk
COPY gthnk_web /usr/local/src/gthnk/gthnk_web
COPY scripts /usr/local/src/gthnk/scripts
COPY setup.py /usr/local/src/gthnk
COPY MANIFEST.in /usr/local/src/gthnk
RUN /opt/gthnk/.venv/bin/pip3 install --disable-pip-version-check --no-cache-dir '/usr/local/src/gthnk[server]' && chown -R gthnk:gthnk /opt/gthnk/.venv

USER gthnk
WORKDIR /opt/gthnk
RUN mkdir -p /opt/gthnk/.config/gthnk
RUN /opt/gthnk/.venv/bin/gthnk config /opt/gthnk/var > /opt/gthnk/.config/gthnk/gthnk.conf
RUN echo 'source /opt/gthnk/.venv/bin/activate' >> /opt/gthnk/.bashrc

ENV FLASK_ENV=production
ENV FLASK_RUN_PORT=1620
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_APP=gthnk_web.app
CMD .venv/bin/flask run

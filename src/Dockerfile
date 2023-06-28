FROM python:3.11-slim-bookworm

# Add application user
RUN adduser \
  --home "/opt/gthnk" \
  --uid 1000 \
  --disabled-password \
  "gthnk"

RUN python3 -m venv /opt/gthnk/.venv
RUN /opt/gthnk/.venv/bin/pip3 install \
  --disable-pip-version-check \
  --no-cache-dir \
  'python-dotenv' \
  'rich' \
  'trogon' \
  'jinja2<3.1.0' \
  'flask==1.1.2' \
  'werkzeug==2.0.3' \
  'Markdown<3.2' \
  'itsdangerous==2.0.1' \
  'Flask-WTF' \
  'flask-markdown' \
  'mdx-linkify==1.0' \
  'mdx-journal>=0.1.4' && \
  chown -R gthnk:gthnk /opt/gthnk/.venv

RUN mkdir /usr/local/src/gthnk
COPY MANIFEST.in /usr/local/src/gthnk
COPY setup.py /usr/local/src/gthnk
COPY scripts /usr/local/src/gthnk/scripts
COPY gthnk_web /usr/local/src/gthnk/gthnk_web
COPY gthnk /usr/local/src/gthnk/gthnk
RUN /opt/gthnk/.venv/bin/pip3 install \
  --disable-pip-version-check \
  --no-cache-dir '/usr/local/src/gthnk[server]' && \
  chown -R gthnk:gthnk /opt/gthnk/.venv

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

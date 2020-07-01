# syntax = docker/dockerfile:experimental

# docker-gthnk
# Ian Dennis Miller

FROM iandennismiller/python:latest

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Add application user
RUN adduser \
  --home "/home/gthnk" \
  --uid 1000 \
  --gecos "gthnk" \
  --disabled-password \
  "gthnk"

# Copy home directory structure
RUN mkdir -p /home/gthnk/.local
RUN mkdir -p /home/gthnk/.local/mnt/shared

COPY src/docker/bin/ /home/gthnk/.local/bin
COPY . /home/gthnk/gthnk
RUN chown -R gthnk:gthnk /home/gthnk

# Install Gthnk
RUN --mount=type=cache,target=/home/gthnk/.cache/pip sudo -i -u gthnk pip3 install --user /home/gthnk/gthnk

# 1) Generate configuration if necessary
# 2) Launch the Gthnk server
CMD if [ ! -f /home/gthnk/.local/mnt/shared/gthnk.conf ]; then \
  sudo -i -u gthnk gthnk-firstrun.sh /home/gthnk/.local/mnt/shared/gthnk.conf; \
  fi; \
  sudo -i -u gthnk gthnk-server.sh

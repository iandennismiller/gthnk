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
RUN mkdir -p /home/gthnk/.gthnk

# Install Gthnk Requirements
COPY requirements.txt /home/gthnk/gthnk/
RUN sudo -i -u gthnk pip3 install --user -r /home/gthnk/gthnk/requirements.txt

COPY src/docker/bin/ /home/gthnk/.local/bin
RUN chown -R gthnk:gthnk /home/gthnk/.local/bin

COPY bin/ /home/gthnk/gthnk/bin
COPY src/ /home/gthnk/gthnk/src
COPY setup.py /home/gthnk/gthnk/
COPY Readme.rst /home/gthnk/gthnk/

# Install Gthnk
RUN sudo -i -u gthnk pip3 install --user /home/gthnk/gthnk

# 1) Generate configuration if necessary
# 2) Launch the Gthnk server
CMD if [ ! -f /home/gthnk/.gthnk/gthnk.conf ]; then \
  sudo -i -u gthnk gthnk-firstrun.sh /home/gthnk/.gthnk/gthnk.conf; \
  fi; \
  sudo -i -u gthnk gthnk-server.sh

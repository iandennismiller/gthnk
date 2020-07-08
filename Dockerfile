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
COPY src/requirements.txt /home/gthnk/
RUN sudo -i -u gthnk pip3 install --user -r /home/gthnk/requirements.txt

COPY src/docker/bin/ /home/gthnk/.local/bin
RUN chown -R gthnk:gthnk /home/gthnk/.local/bin

# Install Gthnk
COPY src/ /home/gthnk/gthnk/src
RUN sudo -i -u gthnk pip3 install --user /home/gthnk/gthnk/src

# 1) Generate configuration if necessary
# 2) Launch the Gthnk server
CMD sudo -i -u gthnk sh -c 'gthnk-firstrun.sh /home/gthnk/.gthnk; gthnk-server.sh'

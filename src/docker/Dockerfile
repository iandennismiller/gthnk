# docker-gthnk
# Ian Dennis Miller

FROM iandennismiller/python:latest

# Add application user
RUN adduser \
  --home "/home/gthnk" \
  --uid 1000 \
  --gecos "gthnk" \
  --disabled-password \
  "gthnk"

# Copy home directory structure
RUN mkdir -p /home/gthnk/.local/bin
COPY bin/ /home/gthnk/.local/bin
RUN chown -R gthnk:gthnk /home/gthnk

# Initialize storage path
RUN mkdir /home/gthnk/storage && chown gthnk:gthnk /home/gthnk/storage

# Legacy; supports logging, somehow...
RUN mkdir /var/lib/gthnk && chown gthnk:gthnk /var/lib/gthnk

# Set up the virtual environment
RUN sudo -i -u gthnk virtualenv -p /usr/bin/python3.7 /home/gthnk/venv

# Clone the git repo
RUN sudo -i  -u gthnk git clone https://github.com/iandennismiller/gthnk.git

# Install Gthnk
RUN sudo -i -u gthnk /home/gthnk/venv/bin/pip install /home/gthnk/gthnk

# Initialize the container with a configuration and database
RUN sudo -i -u gthnk gthnk-firstrun.sh /home/gthnk/storage/gthnk.conf

# 1) Generate configuration if necessary
# 2) Launch the Gthnk server
CMD if [ ! -f /home/gthnk/storage/gthnk.conf ]; then \
  sudo -i -u gthnk gthnk-firstrun.sh /home/gthnk/storage/gthnk.conf; \
  fi; \
  sudo -i -u gthnk gthnk-server.sh

FROM python:3-slim

COPY . /opt/terrain/

RUN python3 -m pip install -r /opt/terrain/requirements.txt \
    && ln -s /opt/terrain/terrain.py /usr/bin/terrain

ENTRYPOINT bash

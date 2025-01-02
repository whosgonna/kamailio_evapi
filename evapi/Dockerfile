# Get the latest base image for python
FROM python:3.13-alpine3.21

RUN <<EOL
    apk add --no-cache tcpdump
    pip install aiohttp asyncio pynetstring
EOL


COPY ./evapi.py /evapi/evapi.py

WORKDIR /evapi


ENTRYPOINT ["python3", "/evapi/evapi.py"]

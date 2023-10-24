FROM golang:1.21 AS supercronic
RUN apt update && \
    apt install -y git && \
    git clone --depth 1 --branch v0.2.27 https://github.com/aptible/supercronic.git && \
    cd supercronic && \
    go build -o /tmp/supercronic main.go && \
    rm -rf ../supercronic && \
    apt purge -y git && \
    apt autoremove -y && \
    rm -rf /var/lib/apt/lists/*

FROM python:3.12-slim
COPY --from=supercronic /tmp/supercronic /usr/local/bin/supercronic

ADD pyproject.toml poetry.lock .

RUN python -m pip install poetry && \
    poetry install

ADD from_my_ex/ .
CMD  ["poetry", "run", "python", "-m", "from_my_ex"]

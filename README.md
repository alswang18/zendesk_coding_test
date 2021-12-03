# Readme for Zendesk Coding

## Configure /ZENDESK_CODING_TEST/ticket_viewer/.env.template!

### Deployed example:

[http://3.96.80.18:8004/](http://3.96.80.18:8004/?page=1)

## Run within Container

### Prerequisites

- Docker
- Docker Compose

### Run the following Script

```bash
docker-compose up --build -d
```

Go to localhost:8004

## Run within Ubuntu or WSL-Ubuntu

### Prerequisites

- Python (^3.8)
- Poetry
- make

### Run the following Script

```bash
apt-get update && apt-get -y install netcat gcc make && apt-get clean
pip install poetry==1.1.11
poetry install

# This repo runs a lot of scripts using the Makefile, so please read it to understand 
# what these commands do
# just run tests, can put .env details in CLI if you don't want to configure it.
make demo-script-test

# run the app, can put .env details in CLI if you don't want to configure it.
make demo-script-run

# before committing changes, run the following and make sure everything passes
make pre-commit
make test
```

**Go to localhost:8000**

### Viable pages:

[localhost:8000](http://localhost:8000) [list view]

[localhost:8000/ticket/<int:ticket_id>](http://localhost:8000/ticket/<int:ticket_id>) [detail view]

HTML Templates Sourced and Inspired by the wonderful people at [Tailblocks](https://web.archive.org/web/20211115132515/https://tailblocks.cc/).

Current output of make test command

![Untitled](Readme%20for%20Zendesk%20Coding%20ccdc0c1fed584c07ab08111f0fe49b3f/Untitled.png)

```bash

```
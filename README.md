# Readme for Zendesk Coding

## Configure /ZENDESK_CODING_TEST/ticket_viewer/.env.template!

## Run within Container

### Prerequisites

- Docker
- Docker Compose

### Run the following Script

```bash
docker-compose --build up
```

Go to localhost:8004

### Run within Ubuntu or WSL-Ubuntu

- Python (^3.8)
- Poetry
- make

### Run the following Script

```bash
apt-get update && apt-get -y install netcat gcc make && apt-get clean
pip install poetry==1.1.11
poetry install

# just run tests, can put .env details in CLI if you don't want to configure it.
make demo-script-test

# run the app, can put .env details in CLI if you don't want to configure it.
make demo-script-run
```

**Go to localhost:8000**

### Viable pages:

[localhost:8000](http://localhost:8000) [list view]

[localhost:8000/ticket/<int:ticket_id>](http://localhost:8000/ticket/<int:ticket_id>) [detail view]
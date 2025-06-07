VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

all: setup certs

# Set up virtual environment and install dependencies
setup:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install aioquic

# Generate TLS certificates
certs:
	mkdir -p certs
	openssl req -newkey rsa:2048 -nodes -keyout certs/key.pem -x509 -days 365 -out certs/cert.pem -subj "/CN=localhost"

# Run the server
server:
	PYTHONPATH=. $(PYTHON) server/server.py

# Run the client
client:
	PYTHONPATH=. $(PYTHON) client/client.py

clean:
	rm -rf $(VENV) certs __pycache__ */__pycache__

.PHONY: all setup certs server client clean

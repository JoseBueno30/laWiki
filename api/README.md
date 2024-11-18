# laWiki microservices

These endpoints were created using OpenApiGenerator.

## Requirements.

Python >= 3.7. Recommened Python 3.12

## Installation & Usage (specific service)

To run an specific server, please execute the following from the root directory:

```bash
cd {microservices/specifici_microservice}
pip3 install -r requirements.txt

# Set the path to the src directory

PYTHONPATH=src # on Linux or macOS
set PYTHONPATH=src # on Windows CMD
$env:PYTHONPATH="src" # on Windows PowerShell

# Then run the server
uvicorn openapi_server.main:app --host 0.0.0.0 --port 8080
```

and open your browser at `http://localhost:8080/docs/` to see the docs.

## Access the database

We are using a MongoDB Atlas databse. To try out the endpoints, add the cluster with the following link: `mongodb+srv://lawiki:lawiki@lawiki.vhgmr.mongodb.net/`

## Running with Docker

To all servers on a Docker container, please execute the following from the root directory:

```bash
docker-compose up --build
```
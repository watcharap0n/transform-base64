# Run FastAPI | Deploy on Docker container

`Structure directory`

```bash
-> application

|-- signature_service
|   |-- app
|   |   |-- __init__.py
|   |   |-- api
|   |   |-- schema
|   |   |__ main.py
|-- |-- Dockerfile
|-- docker-compose.yml

|-- root -> /app/
```

**install dependencies Python**

    $ python -m venv venv
    $ source venv/scripts/activate | ./venv/scripts/activate
    $ pip install -r dashboard_user/requirements.txt
    $ pip install -r register_user/requirements.txt

**testing run server on localhost signature_service port 8000**

    $ cd signature_service
    $ uvicorn app.main:app --port 8001 --reload

**Run docker container**

    $ docker compose up -d

**You can run reverse proxy this url**

    https://localhost:8080/api/base64/docs

**Setup install dependencies instance**

    $ sudo apt-get update
    $ sudo apt install -y python3-pip nginx
    $ sudo apt install docker.io
    $ sudo apt install docker-compose









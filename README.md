# Todo

This app is using Flask as a web framework and Sqlite database as a data storage. Here are the functionalities
-Add new todo
- Edit existing todo
- Mark as Done/canceled
- Delete todo
- Download all todos as `.csv`
- Import todos from csv file

## Dependencies
- Python 3
- Pip 3
- Sqlite

## How does it work

This app is using Flask as a web framework and Sqlite database as a data storage, you need to run these commands to run the development environment

- `pip3 install --no-cache-dir -r requirements.txt`
- `python3 -c "from db import init_db; init_db()"`
- `export FLASK_APP=todo.py`
- `flask run --debug`

Congrats, now the app is up and running, you can access the side from this url `http://127.0.0.1:5000/`

## API

All these functionalities can be used an API endpoints

- List todos `GET` `/api/todos`
- Show todo `GET` `/api/todos/<id>`
- Mark as done/canceled `POST` `/api/todos/<id>/done` `/api/todos/<id>/cancel`
- Delete Todo `POST` `/api/todos/<id>/delete`
- Create/update todo `POST` `/api/todos` `/api/todos/<id>/edit`
```commandline
{
    "title": "New title",
    "description": "new description",
    "due_to": "2024-03-03"
}
```


## Docker
If you don't want to install all the dependencies, you can use docker to run the container, you just need to have `docker` installed in your machine then follow these instructions

- Build the image by running `docker build -t todo .`
- Then run the container by running `docker run  -p 5000:5000 todo`

Congrats, now the app is up and running, you can access the side from this url `http://127.0.0.1:5000/`

## Deployment

This app is deployed to a remote server, you can use the app by visiting this url

- http://todo.omarosama.nl
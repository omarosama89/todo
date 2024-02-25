FROM python:3.9-slim

WORKDIR /todo

COPY . /todo

RUN pip install --no-cache-dir -r requirements.txt

RUN python -c "from db import init_db; init_db()"

EXPOSE 5000

ENV FLASK_APP=todo.py

CMD ["flask", "run", "--host=0.0.0.0"]

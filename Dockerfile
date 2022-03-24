FROM python:3.7-alpine

WORKDIR /app

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN pip install --upgrade pip
COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv
RUN pipenv lock --requirements > requirements.txt
RUN apk add --no-cache zlib-dev jpeg-dev gcc musl-dev linux-headers
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
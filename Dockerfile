FROM python:3.10.5
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/fastapi-docker
COPY Pipfile Pipfile.lock ./

RUN pip install -U pipenv
RUN pipenv install --system

COPY . .

EXPOSE 8001

RUN chmod +x entrypoint.sh

CMD ./entrypoint.sh
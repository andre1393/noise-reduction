FROM python:3.7-slim-buster

RUN mkdir /home/app/

WORKDIR /home/app/

COPY ./Pipfile ./
COPY ./Pipfile.lock ./

RUN apt-get update \
 && apt-get install -y --no-install-recommends python3-dev gcc g++ \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pipenv \
 && pipenv install --system --deploy --ignore-pipfile

COPY . .

RUN pylint noise_reduction --init-hook='import sys; sys.path.append(".")' --errors-only \
 && pytest
EXPOSE 8000

ENTRYPOINT ["sh", "entrypoint.sh"]

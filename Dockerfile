FROM python:3.7-buster

RUN mkdir /home/app/

WORKDIR /home/app/

COPY ./Pipfile ./
COPY ./Pipfile.lock ./
COPY ./requirements.txt ./

RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc g++ \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

#RUN python -m pip install --upgrade pip \
# && pip install --upgrade pip \
# && pip install --no-cache-dir pipenv \
# && pipenv install --system --deploy --ignore-pipfile --verbose
RUN pip install -r requirements.txt -v
COPY . .

RUN pylint audio_processor --init-hook='import sys; sys.path.append(".")' --errors-only \
 && pytest
EXPOSE 8000

ENTRYPOINT ["sh", "entrypoint.sh"]

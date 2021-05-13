# noise-reduction
This project aims to process audio files by reducing noises and calculating metadata such as modal note


## 1. Run locally
### 1.1 run using python
````shell
pipenv install
gunicorn -c gunicorn.py --log-level 'info' --timeout 120 noise_reduction.api.app:app
````
### 1.1 run using docker
````shell
docker build -t noise-reduction .
docker run -it -p 8000:8000 noise-reduction
````

### 1.2 run using docker-compose
```shell
docker-compose up --build
```

## run audio processing
To call the API run the following command:
````shell
curl --location --request POST 'localhost:8000/process-audio' \
--form 'audio_file=@"<audio_file_path>/<audio_filename>.wav"'
````

expected result:
```shell
{
  "status":"OK",
  "filename":"<audio_filename>.wav",
  "audio_length":1104,
  "frequencies": {
    "32.703194":188,
    "329.627533":120,
    ...
    "311.126984":108
    }
}
```
## 2. tests
```shell
pipenv install
pytest
```


## 2. FAQ
### 2.1 update requirements
update requirement in Pipfile and then update Pipfile.lock:
````shell
pipenv lock
````
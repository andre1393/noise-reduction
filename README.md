# audio-processor
This project aims to process audio files by reducing noises and calculating metadata such as modal note

This project depends on the following libraries:
* denoiser: for audio noise reduction
* ffmpeg: for audio conversion
* crepe: for audio frequencies extraction

- [audio-processor](#audio-processor)
    * [1. Run locally](#1-run-locally)
        + [1.1 run using python](#11-run-using-python)
        + [1.1 run using docker](#11-run-using-docker)
        + [1.2 run using docker-compose](#12-run-using-docker-compose)
    * [2. run audio processing](#2-run-audio-processing)
    * [3. tests](#3-tests)
    * [4. lint](#4-lint)
    * [5. FAQ](#5-faq)
        + [5.1 update requirements](#51-update-requirements)
        + [5.2 why python 3.7?](#52-why-python-37-)

## 1. Run locally
### 1.1 run using python
````shell
pipenv install
gunicorn -c gunicorn.py --log-level 'info' --timeout 120 audio_processor.api.app:app
````
### 1.1 run using docker
````shell
docker build -t audio-processor .
docker run -it -p 8000:8000 audio-processor
````

### 1.2 run using docker-compose
```shell
docker-compose up --build
```

## 2. run audio processing
To call the API run the following command:
````shell
curl --location --request POST 'localhost:8000/process' \
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
## 3. tests
```shell
pipenv install
pytest
```

## 4. lint
````shell
pipenv install
pylint audio_processor --init-hook='import sys; sys.path.append(".")'
````


## 5. FAQ
### 5.1 update requirements
update requirement in Pipfile and then update Pipfile.lock:
````shell
pipenv lock
````
### 5.2 why python 3.7?
tensorflow has not a stable version for python 3.9
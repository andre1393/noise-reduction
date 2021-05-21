# audio-processor
This project aims to process audio files by reducing noises and calculating metadata such as modal note

- [audio-processor](#audio-processor)
    * [1. Description](#1-description)
    * [2. Run locally](#2-run-locally)
        + [2.1 run using python](#21-run-using-python)
        + [2.2 run using docker](#22-run-using-docker)
        + [2.3 run using docker-compose](#23-run-using-docker-compose)
    * [3. run audio processing](#3-run-audio-processing)
        + [3.1. /denoise](#31--denoise)
        + [3.2. /modal-frequencies](#32--modal-frequencies)
        + [3.3. /process](#33--process)
    * [4. tests](#4-tests)
    * [5. lint](#5-lint)
    * [6. FAQ](#6-faq)
        + [6.1 update requirements](#61-update-requirements)
        + [6.2 why python 3.7?](#62-why-python-37-)
    
## 1. Description
This project depends on the following libraries:
* denoiser: for audio noise reduction
* ffmpeg: for audio conversion
* crepe: for audio frequencies extraction

## 2. Run locally
### 2.1 run using python
````shell
pipenv install
gunicorn -c gunicorn.py --log-level 'info' --timeout 120 audio_processor.api.app:app
````
### 2.2 run using docker
````shell
docker build -t audio-processor .
docker run -it -p 8000:8000 audio-processor
````

### 2.3 run using docker-compose
```shell
docker-compose up --build
```

## 3. run audio processing
There are 3 available API form audio processing:
- /denoise: apply denoiser algorithm to audio and return enhanced audio
- /modal-frequencies: apply crepe algorithm to audio and return modal frequencies
- /process: apply denoiser and crepe algorithm and return enhanced audio and modal frequencies as header in key `frequencies`

### 3.1. /denoise
To call the API run the following command:
````shell
curl --location --request POST 'localhost:8000/denoise' \
--form 'audio_file=@"<audio_file_path>/<audio_filename>.wav"' \
--form 'convert_audio="true"'
````
expected result:
enhanced_audio at body

### 3.2. /modal-frequencies
To call the API run the following command:
````shell
curl --location --request POST 'localhost:8000/modal-frequencies' \
--form 'audio_file=@"<audio_file_path>/<audio_filename>.wav"'
````
expected body, should be similar to the following:
````shell
{"frequencies":{"32":26,"52":6,"34":4,"56":3,"55":3,"647":3,"648":3,"651":3,"31":2,"48":2}}
````

### 3.3. /process
To call the API run the following command:
````shell
curl --location --request POST 'localhost:8000/denoise' \
--form 'audio_file=@"<audio_file_path>/<audio_filename>.wav"' \
--form 'convert_audio="true"'
````
expected result:
enhanced_audio at body and the and headers similar to the following
````shell
HTTP/1.1 200 OK
date: Fri, 21 May 2021 20:21:42 GMT
server: uvicorn
frequencies: {32: 26, 52: 6, 34: 4, 56: 3, 55: 3, 647: 3, 648: 3, 651: 3, 31: 2, 48: 2}
content-type: audio/wav
content-length: 109582
last-modified: Fri, 21 May 2021 20:21:44 GMT
etag: 8b1e35a083dbd0e89b5c5987c3f0a29c
````


## 4. tests
```shell
pipenv install
pytest
```

## 5. lint
````shell
pipenv install
pylint audio_processor --init-hook='import sys; sys.path.append(".")'
````


## 6. FAQ
### 6.1 update requirements
update requirement in Pipfile and then update Pipfile.lock:
````shell
pipenv lock
````
### 6.2 why python 3.7?
tensorflow has not a stable version for python 3.9

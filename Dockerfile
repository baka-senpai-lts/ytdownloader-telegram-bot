FROM python:3.8.5

RUN mkdir /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip3 install -r requirments.txt
COPY fix_cipher_error.py /usr/local/lib/python3.8/site-packages/pytube/extract.py

RUN apt-get update
RUN apt-get -yq install ffmpeg

CMD [ "python3", "-u", "app.py" ]

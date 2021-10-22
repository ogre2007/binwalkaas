# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /binwalk

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
RUN https://github.com/ReFirmLabs/binwalk && cd binwalk
RUN sudo python3 setup.py install --prefix ~/.local && cd .. && rm -rf binwalk
COPY . .

ENV FLASK_APP /app/app.py

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port 5555"]

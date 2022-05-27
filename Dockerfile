FROM python:3.9.7

WORKDIR /usr/scr/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

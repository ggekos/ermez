FROM python:3.10-rc

RUN apt-get -y update

WORKDIR /home/app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENV PYTHONUNBUFFERED definitely

CMD ["python3", "etlm/main.py"]

FROM python:3.11

ENV DockerHOME=/home/apps/15min-user-api/

RUN mkdir -p $DockerHOME

RUN apt-get update -y -q
RUN apt-get install python3-dev default-libmysqlclient-dev build-essential -y -q

WORKDIR $DockerHOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY . $DockerHOME
RUN pip install -r requirements.txt
EXPOSE 8001

RUN chmod +x /home/apps/15min-user-api/start.sh
CMD ["./start.sh"]
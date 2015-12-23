FROM debian:jessie
RUN apt-get -y update && \
	apt-get install -y build-essential python3.4 python3-dev python3-setuptools git
RUN easy_install3 pip

ADD . /build/
WORKDIR /build/

RUN pip3 install -r requirements.txt

VOLUME /build/Application/static/uploads/
EXPOSE 8000
CMD gunicorn -c gunicorn.py Application:app
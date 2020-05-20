FROM python:3.8

COPY ./autopost /srv/autopost
COPY ./requirements.txt /srv/autopost/r.txt

WORKDIR /srv/

RUN pip3 install -r /srv/autopost/r.txt

CMD python3 -u autopost/ rules.yml
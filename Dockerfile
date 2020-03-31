FROM tiangolo/uwsgi-nginx-flask:python3.7
RUN apt-get update \
    && apt-get install -y libsm6 mc\
    && apt-get clean
RUN pip install --upgrade pip
COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt

RUN rm -r /root/.cache

ENV STATIC_URL /static
ENV STATIC_PATH /app/app/static

COPY ./ /app
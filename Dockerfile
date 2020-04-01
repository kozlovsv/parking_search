FROM tiangolo/uwsgi-nginx-flask:python3.7
RUN apt-get update \
    && apt-get install -y libsm6 mc\
    && apt-get clean
RUN pip install --upgrade pip
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN rm -r /root/.cache

COPY ./server-conf/nginx.conf /etc/nginx/

ENV STATIC_URL /static
ENV STATIC_PATH /app/app/static

COPY ./ /app
RUN chown -R nginx:nginx /app
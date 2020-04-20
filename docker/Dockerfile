FROM kozlovsv78/openvino
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
RUN yum update -y \
    && yum clean all
ENV APP_DIR /opt/parking
WORKDIR $APP_DIR
COPY ./requirements.txt $APP_DIR/requirements.txt
RUN pip3 install -r $APP_DIR/requirements.txt \
    && rm -r /root/.cache

# copy project
COPY ./ $APP_DIR/

ENTRYPOINT ["bash", "/opt/parking/docker/conf/app/entrypoint.sh"]
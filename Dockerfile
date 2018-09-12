FROM ubuntu

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y && \
    apt-get install -y python \
                       python-pip \
                       python-tk \
                       && \
    apt-get clean all

RUN pip install flask \
                Flask-SQLAlchemy \
                pymongo \
                psycopg2 \
                pytz \
                tzlocal \
                pandas \
                numpy \
                matplotlib

ADD trackibs /trackibs

EXPOSE 5000
WORKDIR /trackibs

CMD ["flask","run","--host=0.0.0.0"]

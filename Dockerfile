FROM ubuntu:latest as builder

RUN apt-get -yqq update \
&& apt-get -yqq install python3-pip python3-dev \
&& cd /usr/local/bin \
&& ln -s /usr/bin/python3 python \
&& pip3 install --upgrade pip

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip3 wheel -r requirements.txt -w /wheels

FROM ubuntu:latest
RUN apt-get -yqq update \
&& apt-get -yqq install python3-pip python3-dev \
&& cd /usr/local/bin \
&& ln -s /usr/bin/python3 python \
&& pip3 install --upgrade pip

WORKDIR /app

COPY --from=builder /wheels /wheels
COPY requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt --find-links /wheels

COPY . /app
ENV PYTHONPATH /app

WORKDIR /app/features

CMD ["behave"]


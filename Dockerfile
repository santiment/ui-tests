FROM python:3.7.4-alpine as builder

RUN apk update && \
apk add alpine-sdk python-dev

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip wheel -r requirements.txt -w /wheels

FROM python:3.7.4-alpine
RUN apk update && \
apk add alpine-sdk python-dev

WORKDIR /app

COPY --from=builder /wheels /wheels
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt --find-links /wheels

COPY . /app
ENV PYTHONPATH /app

WORKDIR /app/features

CMD ["behave"]


FROM python:3.12-alpine

WORKDIR /app/clip_joy

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./myvlog .

RUN pip install --upgrade pip

RUN apk add --update --no-cache-dir --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

RUN pip install --no-cache-dir -r requirements.txt



#CMD ["gunicorn", "-b", "0.0.0.0:8001", "myvlog.myvlog.wsgi:application"]
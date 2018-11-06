FROM python:3.6-alpine

COPY ./rootfs/app/requirements.txt /app/
RUN pip install -r /app/requirements.txt && rm -rf /tmp/* /var/tmp/* /root/.cache
COPY ./rootfs/app /app

WORKDIR /app

ENV MONGO_URI="mongodb://mongodb:27017/logosmart?ssl=false&ssl_cert_reqs=CERT_NONE" \
    FLASK_ENV="production" \
    WEB_CONCURRENCY="1"

EXPOSE 80

CMD ["gunicorn", "-c", "config.py", "server:app"]

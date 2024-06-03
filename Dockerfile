FROM python:3.10

ARG APP_NAME
ARG APP_PORT
RUN mkdir -p "/usr/src/${APP_NAME}_backend"
WORKDIR "/usr/src/${APP_NAME}_backend"

COPY ./requirements.txt "/usr/src/${APP_NAME}_backend"
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . "/usr/src/${APP_NAME}_backend"
EXPOSE ${APP_PORT}

COPY ./migrations-on-startup.sh /app/
RUN ["chmod", "+x", "/app/migrations-on-startup.sh"]
ENTRYPOINT ["/app/migrations-on-startup.sh"]

CMD gunicorn -w 4 -b 0.0.0.0:${APP_PORT} -k uvicorn.workers.UvicornWorker main:app --graceful-timeout 400

FROM python:3.9-slim

WORKDIR /app

COPY voiture/requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . ./

ENV PYTHONUNBUFFERED=1


CMD sleep 10 && \
    python voiture/manage.py collectstatic --noinput && \
    python voiture/manage.py migrate && \
    # python voiture/manage.py createsuperuser \
    #     --email "admin@admin.admin" --username "admin" --noinput && \
    # python voiture/manage.py shell < voiture/voiture/super.py && \
    python voiture/manage.py runserver 0.0.0.0:8080


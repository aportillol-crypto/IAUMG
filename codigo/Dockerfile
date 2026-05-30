FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=production
ENV DB_HOST=db
ENV DB_PORT=5432
ENV DB_NAME=tienda_db
ENV REDIS_URL=redis://cache:6379/0

EXPOSE 5000

CMD ["python", "app.py"]

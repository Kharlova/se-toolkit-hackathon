FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN mkdir -p data

EXPOSE 8000

CMD ["python", "app.py"]

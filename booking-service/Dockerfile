FROM python:3.13.1-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y postgresql-client

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x entrypoint.sh

CMD ["sh", "./entrypoint.sh"]

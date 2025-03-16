FROM python:3.13.1-slim

WORKDIR /app

COPY . .

# Install PostgreSQL client (for pg_isready)
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["sh", "./entrypoint.sh"]

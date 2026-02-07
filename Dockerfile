# Xenon Dockerfile
FROM python:3.12-slim


RUN apt-get update && apt-get install -y curl

WORKDIR /app

# Copy all source files
COPY . /app/

# Install pipenv and dependencies
RUN pip install pipenv && pipenv install --deploy --system

EXPOSE 5000

RUN chmod +x /app/start.sh
CMD ["/app/start.sh"]

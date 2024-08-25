FROM python:3.8

WORKDIR /dv-english-api
COPY ./requirements.txt /dv-english-api/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /dv-english-api/requirements.txt

# Copy the application code
COPY ./app /dv-english-api/app
COPY ./db /dv-english-api/db
COPY ./migrations /dv-english-api/migrations
COPY ./models /dv-english-api/models
COPY ./alembic.ini /dv-english-api/alembic.ini
COPY ./README.md /dv-english-api/README.md

# Copy the .env file
COPY ./app/.env /dv-english-api/app/.env
COPY ./app/.env /dv-english-api/migrations/.env
COPY ./app/.env /dv-english-api/db/.env

# Set environment variable from .env file
ENV $(cat /dv-english-api/app/.env | xargs)

# Run Alembic migration
RUN alembic upgrade head

# Command to run the application
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80" ]
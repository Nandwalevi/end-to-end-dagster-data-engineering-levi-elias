FROM python:3.11-slim

# system deps + build deps for psycopg2 in one layer
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# copy dependency lists first (Docker layer cache)
COPY requirements.txt requirements-dev.txt ./

# upgrade pip + install Python deps
RUN python -m pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

# copy the rest of the project
COPY . .

ENV PYTHONPATH=/workspace

# keep container alive for dev-container
CMD ["sleep", "infinity"]
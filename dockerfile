# === Stage 1: build stage ===
FROM python:3.8-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y curl build-essential gcc

COPY requirements.txt .

# Install dependencies into a custom folder
RUN pip install --upgrade pip && \
    pip install --prefix=/install "setuptools<58.0.0" && \
    pip install --prefix=/install -r requirements.txt && \
    pip install --prefix=/install playwright

# === Stage 2: final image ===
FROM python:3.8-slim

ENV FLASK_ENV=development

WORKDIR /app

# Copy installed packages from builder stage
COPY --from=builder /install /usr/local

# Install playwright system dependencies and browser
RUN apt-get update && \
    apt-get install -y curl && \
    playwright install-deps && \
    playwright install chromium && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 5000

CMD ["python3.8", "-u", "run.py"]

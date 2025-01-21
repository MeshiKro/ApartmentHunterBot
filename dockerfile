FROM python:3.8-slim

ENV FLASK_ENV=development


WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    for pkg in libglib2.0-0 libnss3 libnspr4 libdbus-1-3 libatk1.0-0 \
               libatk-bridge2.0-0 libcups2 libdrm2 libxcb1 libxkbcommon0 \
               libatspi2.0-0 libx11-6 libxcomposite1 libxdamage1 libxext6 \
               libxfixes3 libxrandr2 libgbm1 libpango-1.0-0 libcairo2 libasound2; do \
        if ! dpkg -s $pkg >/dev/null 2>&1; then \
            echo "Installing $pkg..."; \
            apt-get install -y $pkg || echo "Failed to install $pkg, continuing..."; \
        else \
            echo "$pkg is already installed, skipping..."; \
        fi; \
    done && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Playwright and its dependencies
# RUN pip install playwright && playwright install-deps && playwright install
RUN pip install playwright && playwright install chromium

COPY . .

EXPOSE 5000

CMD ["python3.8", "-u", "run.py"]

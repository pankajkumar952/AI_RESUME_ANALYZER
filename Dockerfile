FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Prevent Python from creating .pyc files
# and ensure logs are shown immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
# - Tesseract OCR
# - Poppler for PDF processing
# - Chromium + ChromeDriver for Selenium
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    libpoppler-dev \
    chromium \
    chromium-driver \
    wget \
    unzip \
    curl \
    xvfb \
    fontconfig \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcairo2 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to improve Docker layer caching
COPY requirements.txt .

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install spaCy English model
RUN python -m spacy download en_core_web_sm

# Copy application source code
COPY . .

# Create upload directory if required
RUN mkdir -p /app/uploads

# Streamlit port
EXPOSE 8501

# Start Streamlit
CMD [
    "streamlit",
    "run",
    "app.py",
    "--server.port=8501",
    "--server.address=0.0.0.0",
    "--server.headless=true",
    "--server.enableCORS=false",
    "--server.enableXsrfProtection=false
]
# Use the official Python image specialized for headless environments
FROM python:3.10-slim

# Prevent Python from buffering stdout/stderr and writing .pyc files
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory inside the container
WORKDIR /app

# Install native system dependencies:
# - libreoffice suite: Natively converts DOCX, PPTX, XLSX to PDF flawlessly without watermarks
# - fonts-liberation: Ensures format styles don't break during conversion
# - libgdiplus / libc6-dev: Required for pure-Python fallback modules like Aspose
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libreoffice \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress \
    fonts-liberation \
    libgdiplus \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the dependencies file and install them natively
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire API and Frontend to the container
COPY . .

# Expose Render's dynamic port gracefully or default to 5000 naturally
EXPOSE 5000

# Spin up the High-Performance FastAPI Server natively via dynamic ports
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-5000}"]

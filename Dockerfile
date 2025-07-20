FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    ffmpeg \
    libssl-dev \
    libffi-dev \
    build-essential \
    mediainfo \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages with specific versions
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir \
    asyncio \
    motor \
    kurigram \
    pyrogram==2.1.0 \
    python-dotenv==1.0.1 \
    py-tgcalls==2.0.1 \
    youtube-search \
    youtube-search-python \
    yt-dlp \
    Pillow \
    pymediainfo

# Optional: Create a non-root user and switch to it
RUN useradd -m appuser && \
    mkdir -p /app && \
    chown appuser:appuser /app
USER appuser
WORKDIR /app

# Copy requirements first to leverage Docker cache
# COPY --chown=appuser:appuser requirements.txt .
# RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the application
# COPY --chown=appuser:appuser . .

# Set the entry point (adjust as needed)
# CMD ["python3", "main.py"]


#FROM ubuntu:22.04
#RUN apt-get update -y && apt-get upgrade -y \
#    && apt-get install -y --no-install-recommends git ffmpeg python3-pip \
 #   && apt-get clean \
 #   && rm -rf /var/lib/apt/lists/*
#COPY . /app/
#WORKDIR /app/
#RUN pip3 install --no-cache-dir --upgrade --requirement requirements.txt
CMD python3 -m AdityaHalder

# 1. Purane 'buster' ko 'bullseye' se badla (Error Fix)
FROM python:3.9-slim-bullseye

# 2. System update aur ffmpeg install (Fast & Clean)
RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 3. Dependencies install karein
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

# 4. Render Port Fix (Iske bina bot kill ho jata hai)
EXPOSE 10000

# 5. Bot start command
CMD ["python3", "bot.py"]

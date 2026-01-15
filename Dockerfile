# Python 3.9 ko badal kar 3.10 kar diya
FROM python:3.10-slim-bullseye

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends ffmpeg git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["python3", "bot.py"]

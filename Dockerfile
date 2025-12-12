##############################
# Stage 1: Builder
##############################
FROM python:3.11-slim AS builder

WORKDIR /app

COPY requirements.txt .

# Install dependencies into /install
RUN pip install --no-cache-dir --target /install -r requirements.txt
RUN ls -R /install


##############################
# Stage 2: Runtime
##############################
FROM python:3.11-slim AS runtime

ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y --no-install-recommends \
        cron \
        tzdata \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed Python packages
COPY --from=builder /install/ /usr/local/lib/python3.11/site-packages/

# ✅ FIX: Copy uvicorn binary and other scripts
COPY --from=builder /install/bin/* /usr/local/bin/

# Make sure Python can find installed libs
ENV PYTHONPATH="/usr/local/lib/python3.11/site-packages"

COPY . .

RUN chmod 0644 cron/job.cron && crontab cron/job.cron
RUN mkdir -p /data /cron

EXPOSE 8080

CMD ["sh", "-c", "cron && uvicorn api:app --host 0.0.0.0 --port 8080"]

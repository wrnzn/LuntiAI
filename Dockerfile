FROM python:3.11-slim

WORKDIR /code

# Copy requirements & install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create cache dirs for HF (prevents permission errors in Space)
RUN mkdir -p /tmp/cache && chmod 777 /tmp/cache
ENV TRANSFORMERS_CACHE=/tmp/cache
ENV NUMBA_CACHE_DIR=/tmp/cache
ENV MPLCONFIGDIR=/tmp/cache
ENV LUNTIAI_DB_PATH=/tmp/luntiai/users.db
ENV LUNTIAI_DEMO_MODE=true

RUN mkdir -p /tmp/luntiai && chmod 700 /tmp/luntiai

# Copy all files
COPY . .

# Run FastAPI app on HF default port 7860
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]

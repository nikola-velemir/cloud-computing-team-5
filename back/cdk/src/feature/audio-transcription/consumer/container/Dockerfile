FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    wget \
    build-essential \
    libsndfile1 \
    libffi-dev \
    libssl-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
# Upgrade pip

RUN pip install --upgrade pip

# Install CPU versions of torch and torchaudio explicitly
RUN pip install --no-cache-dir torch==2.3.1+cpu torchaudio==2.3.1+cpu --index-url https://download.pytorch.org/whl/cpu

# Then install the rest of the requirements
RUN grep -vE "torch|torchaudio" requirements.txt > temp_requirements.txt
RUN pip install --no-cache-dir -r temp_requirements.txt
RUN python -c "import whisper; whisper.load_model('small', device='cpu')"


COPY lambda.py .

CMD ["lambda.lambda_handler"]

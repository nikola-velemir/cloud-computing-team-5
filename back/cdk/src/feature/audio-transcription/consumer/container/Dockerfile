# Stage 1: Build everything
FROM public.ecr.aws/lambda/python:3.12

# Install tools for ffmpeg extraction
RUN dnf -y install tar xz && dnf clean all

# Copy local ffmpeg archive
COPY ffmpeg-release-amd64-static.tar.xz /tmp/

# Extract and move ffmpeg to /usr/bin
RUN tar xvf /tmp/ffmpeg-release-amd64-static.tar.xz -C /tmp/ && \
    mv /tmp/ffmpeg-*-amd64-static/ffmpeg /usr/bin/ffmpeg && \
    rm -rf /tmp/ffmpeg-release-amd64-static.tar.xz /tmp/ffmpeg-*-amd64-static

# Install numpy
RUN pip install --no-cache-dir numpy==1.26.4

# Copy local wheels
COPY wheels/ /wheels/

# Install PyTorch stack from local wheels, then remove them
RUN pip install --no-cache-dir /wheels/torch-2.2.2+cpu-*.whl \
    /wheels/torchaudio-2.2.2+cpu-*.whl \
    /wheels/torchvision-0.17.2+cpu-*.whl && \
    rm -rf /wheels

# Install Whisper
RUN pip install --no-cache-dir openai-whisper

# Copy your pre-downloaded Whisper model
COPY tiny.pt /models/tiny.pt

# Copy Lambda function
COPY lambda.py ${LAMBDA_TASK_ROOT}

# Set Lambda handler
CMD [ "lambda.lambda_handler" ]

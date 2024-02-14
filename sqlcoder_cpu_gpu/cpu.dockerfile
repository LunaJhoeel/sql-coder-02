FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

SHELL ["/bin/bash", "-o", "pipefail", "-c"] # runpod default images

# Set Work Directory
WORKDIR /app

# ARGs and ENVs
ARG TORCH_HOME=/cache/torch
ARG HF_HOME=/cache/huggingface

# Environment variables
ENV TORCH_HOME=${TORCH_HOME}
ENV HF_HOME=${HF_HOME}

# Set LD_LIBRARY_PATH for library location (if still necessary)
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/aarch64-linux-gnu/
ENV SHELL=/bin/bash
ENV PYTHONUNBUFFERED=True
ENV DEBIAN_FRONTEND=noninteractive

# Update, upgrade, install packages and clean up
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    # Basic Utilities
    build-essential libsqlite3-dev default-libmysqlclient-dev gcc git wget ffmpeg curl espeak-ng

# Python
RUN apt-get install -y --no-install-recommends \
    # Python 3.10 and venv
    software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3.10-venv python3.10-distutils python3-dev libpython3.10-dev && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    # Set locale
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen

# Create and activate virtual environment
RUN python3.10 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

# Copy requirements.txt and install dependencies
COPY requirements.txt .

RUN python3 -m pip install --no-cache-dir --upgrade pip
# Install Python dependencies, setuptools-rust
RUN pip install -r requirements.txt --no-cache-dir

# # Install function torch
# RUN pip install torch==2.1.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu118

# # Install git lfs
# RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
# RUN apt-get install git-lfs

# # Install specific voice packages
# COPY ./reqs/req_text2speech.txt .
# RUN pip install -r req_text2speech.txt
# RUN pip install git+https://github.com/resemble-ai/monotonic_align.git
# RUN git clone https://github.com/yl4579/StyleTTS2.git
# RUN git-lfs clone https://huggingface.co/yl4579/StyleTTS2-LibriTTS

# # Download nltk punkt
# RUN python -m nltk.downloader punkt

# # Copy in the build image dependencies
# COPY . .
# RUN mv StyleTTS2-LibriTTS/Models api/v0_serverless/voice_utils/
# RUN python -c 'from api.v0_serverless.voice_utils.styletts2_en import *'
# RUN mv api/v0_serverless/voice.py handler.py

# ENV TOKENIZERS_PARALLELISM=False

# Download the model
RUN curl -L "https://huggingface.co/defog/sqlcoder-7b-2/resolve/main/sqlcoder-7b-q5_k_m.gguf?download=true" -o /app/sqlcoder-7b-q5_k_m.gguf

COPY . /app

# Set Stop signal and CMD
STOPSIGNAL SIGINT

# Runpod serverless configuration
CMD [ "python", "-u", "handler_cpu.py" ]
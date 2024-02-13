FROM nvidia/cuda:12.2.0-base-ubuntu22.04

WORKDIR /app

COPY ./requirements.txt /app/

# Cache the model
ARG TORCH_HOME=/cache/torch
ARG HF_HOME=/cache/huggingface
ENV TORCH_HOME=${TORCH_HOME}
ENV HF_HOME=${HF_HOME}

# Install Python, pip, and curl
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install CUDA Toolkit
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    cuda-toolkit-12-2 && \
    rm -rf /var/lib/apt/lists/*

# Set the environment variable CUDACXX
ENV CUDACXX=/usr/local/cuda/bin/nvcc

RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Install llama-cpp-python with CMAKE_ARGS for NVIDIA RTX3060
RUN CMAKE_ARGS="-DLLAMA_CUBLAS=on -DCMAKE_CUDA_ARCHITECTURES=86" pip install llama-cpp-python==0.2.39 --verbose --no-cache-dir

# Download the model
RUN curl -L "https://huggingface.co/defog/sqlcoder-7b-2/resolve/main/sqlcoder-7b-q5_k_m.gguf?download=true" -o /app/sqlcoder-7b-q5_k_m.gguf

COPY . /app

CMD ["python3", "main.py"]

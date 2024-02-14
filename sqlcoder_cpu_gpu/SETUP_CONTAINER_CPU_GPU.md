# CPU
## Build image
docker build -t sqlcoder_cpu_image -f cpu.dockerfile .

## Create container
docker run --name sqlcoder_container sqlcoder_cpu_image

# GPU
## Build image
docker build -t sqlcoder_gpu_image -f gpu.dockerfile .

## Create container
docker run --name sqlcoder_container --gpus all sqlcoder_gpu_image
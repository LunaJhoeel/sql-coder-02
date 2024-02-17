# GPU
## Build image
docker build -t sqlcoder_gpu_image -f Dockerfile .

## Create container
docker run --name sqlcoder_container --gpus all sqlcoder_gpu_image
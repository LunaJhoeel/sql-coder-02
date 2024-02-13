## Build image
docker build -t sqlcoder-7b-2_image .

## Create container
docker run --name sqlcoder-7b-2_container --gpus all sqlcoder-7b-2_image
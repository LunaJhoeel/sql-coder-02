# CPU

## Build image
docker build -t sqlcoder_cpu_image -f cpu.dockerfile .

## Create container
docker run --name sqlcoder_container sqlcoder_cpu_image
# NearAI CVM Runner

NEAR AI Agent runner for Confidential Virtual Machines. To be ran in a CVM.

## Build

From nearai root directory:
```bash
# clean build
docker buildx build --no-cache --load --platform linux/amd64 -t nearai_runner:latest -f .docker/Dockerfile.cvm_runner .
# build with cache
docker buildx build --load --platform linux/amd64 -t nearai_runner:latest -f .docker/Dockerfile.cvm_runner .
```

## Build and push

```bash
export OWNER=robortyan
# add tag to build
docker tag nearai_runner:latest ${OWNER}/nearai_cvm_runner:latest
# push image
docker push ${OWNER}/nearai_cvm_runner:latest
```

## Run

```bash
export HOST_PORT=8443
docker run --platform linux/amd64 \
    -p ${HOST_PORT}:443 \
    -e ACCOUNT_ID=ncd-cn.near \
    nearai_runner:latest
```

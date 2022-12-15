# CONTRIBUTING

## How to run the Dockerfile locally (creating volumes)

```
docker run -dp <port_forwarding>:<port_defined> -w /app -v "/c/Documents/yourproject:/app" <docker_image_name>

```

## syntax for installing packages from a txt file

```
pip install -r requirements.txt
```

## build docker image
```
docker build -t <name_of_the_image> .
```

## run docker image
```
docker run -dp <port_forwarding>:<port_defined> <docker_image_name>
```
```
docker run -d <docker_image_name> #? without port-forwarding
```
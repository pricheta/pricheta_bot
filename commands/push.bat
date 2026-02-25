set IMAGE_NAME=prichetaboss/pricheta_bot:latest

docker login
docker build -t %IMAGE_NAME% .
docker push %IMAGE_NAME%
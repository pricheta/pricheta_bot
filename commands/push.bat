@echo off
set IMAGE_NAME=prichetaboss/pricheta_bot:latest

cls
docker login
docker build -t %IMAGE_NAME% .
docker push %IMAGE_NAME%
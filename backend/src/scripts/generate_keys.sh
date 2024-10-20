#!/bin/bash

mkdir -p backend/src/core/certs

openssl genrsa -out app/src/core/certs/jwt-private.pem 2048
echo "Приватный ключ создан: app/src/core/certs/jwt-private.pem"

openssl rsa -in app/src/core/certs/jwt-private.pem -outform PEM -pubout -out app/src/core/certs/jwt-public.pem
echo "Публичный ключ создан: app/src/core/certs/jwt-public.pem"

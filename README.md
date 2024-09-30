# LifeMoney

1. Получать новый access токен при изменении данных пользователя
2. График 
```
1 day from current time = 5-minutely data
2 - 90 days from current time = hourly data
above 90 days from current time = daily data (00:00 UTC)
```

3. Сделать скрипты для добавления миграций, пользователя
4. Подумать над классами портфеля
6. из env token time and db echo

### Запуск
1. Собрать и запустить контейнеры
    ```
        docker compose up -d --build
    ```
2. Применить миграции
    ```
    docker compose exec web alembic -c src/core/db/alembic.ini upgrade head
    ```
3. Сгенирировать public и private ключи
    ```
         docker compose exec web alembic -c src/core/db/alembic.ini upgrade head
   openssl rsa -in app/src/core/certs/jwt-private.pem -outform PEM -pubout -out app/src/core/certs/jwt-public.pem
   ```
4. Скачать токены и активы для стока по путям:
   -http://localhost:8000/docs#/stocks/update_assets_api_v1_stocks_update_assets_get
   -http://localhost:8000/docs#/cryptos/update_token_list_api_v1_cryptos_token_update_get
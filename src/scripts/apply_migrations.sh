#!/bin/bash

alembic -c src/core/db/alembic.ini upgrade head

echo "Миграции успешно применены!"
#!/bin/bash
set -e

# Устанавливаем порт по умолчанию, если он не задан
PGPORT=${PGPORT:-5432}

# Экспортируем переменные окружения для использования в конфигурации
export PGPORT

# Если файл /init.sql существует и база данных не инициализирована, выполняем его
if [ ! -s "$PGDATA/PG_VERSION" ]; then
  echo "Инициализация базы данных..."

  # Инициализация базы данных под пользователем postgres
  gosu postgres /usr/local/bin/docker-entrypoint.sh postgres &

  # Ожидание готовности сервера
  until gosu postgres pg_isready -h localhost -p $PGPORT; do
    echo "Ожидание запуска PostgreSQL..."
    sleep 2
  done

  echo "Создание тестовой базы данных..."
  gosu postgres psql -U "$POSTGRES_USER" -c "CREATE DATABASE \"${TEST_DB_NAME}\";"


  if [ -f /roles.sql ]; then
    echo "Создаются пользоавтели"
    envsubst < /roles.sql > /tmp/processed_roles.sql
    chown postgres:postgres /tmp/processed_roles.sql # Отдаем права на выполнение
    gosu postgres psql -U "$POSTGRES_USER" -f /tmp/processed_roles.sql
  fi


  # Замена переменных и выполнение init.sql
  if [ -f /init.sql ]; then
    echo "Выполняется /init.sql..."
    envsubst < /init.sql > /tmp/processed_init.sql
    chown postgres:postgres /tmp/processed_init.sql
    gosu postgres psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /tmp/processed_init.sql

    echo "Выполняется /init.sql для тестовой базы данных..."
    gosu postgres psql -U "$POSTGRES_USER" -d "$TEST_DB_NAME" -f /tmp/processed_init.sql
  fi


  if [ -f /roots.sql ]; then
    echo "Выдаются права для работы для основной базой данных"
    envsubst < /roots.sql > /tmp/processed_roots.sql
    chown postgres:postgres /tmp/processed_roots.sql
    gosu postgres psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /tmp/processed_roots.sql
    echo "Выдаются права для работы для тестовой базой данных"
    gosu postgres psql -U "$POSTGRES_USER" -d "$TEST_DB_NAME" -f /tmp/processed_roots.sql
  fi

  # Остановка сервера
  gosu postgres pg_ctl -D "$PGDATA" -m fast -w stop
fi

# Запуск сервера на переднем плане под пользователем postgres
exec gosu postgres /usr/local/bin/docker-entrypoint.sh postgres


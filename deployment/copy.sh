#!/bin/bash

# Получаем текущее время в формате ГГГГ-ММ-ДД-ЧЧ-ММ-СС
timestamp=$(date +%Y-%m-%d-%H-%M-%S)

# Директория для копирования
source_dir_backend="mipt_book/backend/backend/pgdb"
source_dir_users="mipt_book/users/authorization/pgdb_users"

mkdir "backup/${timestamp}"

target_dir_backend="backup/${timestamp}/backend"
target_dir_users="backup/${timestamp}/users"

cp -r "$source_dir_backend" "$target_dir_backend"
cp -r "$source_dir_users" "$target_dir_users"


echo "Директория скопирована в: $target_dir_backend"
echo "Директория скопирована в: $target_dir_users"

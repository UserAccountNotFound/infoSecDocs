#!/bin/sh
set -e

# Инициализация проекта если нет конфига
if [ ! -f "/docs/mkdocs.yml" ]; then
    echo "Нет файлов проекта"
    echo "Инициализируем новый проект MkDocs, в качестве заглушки "
    mkdocs new /docs
fi

exec mkdocs "$@"
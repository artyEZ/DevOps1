#!/bin/bash
while true; do
    echo "Запуск webhook-сервера..."
    python3 /home/vboxuser/Desktop/webhook-deployer/webhook_server_try.py
    echo "Сервер завершился. Перезапуск через 5 секунд..."
    sleep 5
done

## Для запуска проекта
    В терминале windows:
    - через WSL | wsl -d Ubuntu
    В терминале Ubuntu:
    sudo systemctl start redis-server
    sudo service mysql start
---
    После чего запускаем manage.py в Web_BarCard через | python manage.py runserver
## Полезные команды
    sudo systemctl status redis-server
    redis-cli
    sudo mysql -u username
    
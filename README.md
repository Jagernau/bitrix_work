## Программа для сбора данных с систем мониторинга.
## Описание:
Программа собирает данные по тс из систем мониторига:
- Glonassoft
- Fort
- Wialon hosting
- Wialon local
- Scout
- ASM ERA
По взаимодействию по Api систем мониторинга и распределяет в базу данных, привязывая объекты через логины Пользователей к Контрагентам 1С фирмы.
## База данных MySQL:
Создать базу данных bitrix_work и админку, 
можно контейнером docker-compose:
version: '3.1'
services:
  db:
    image: mysql:latest
    container_name: db
    restart: always
    command: mysqld --character-set-server=utf8 --collation-server=utf8_unicode_ci --init-connect='SET NAMES UTF8;' --innodb-flush-log-at-trx-commit=0
    environment:
      MYSQL_ROOT_PASSWORD: "Ваш пароль"
      MYSQL_DATABASE: "Имя базы данных"
      MYSQL_USER: "Имя пользователя"
      MYSQL_PASSWORD: "Пароль пользователя"
    ports:
      - "Ваш порт:3306"
    volumes:
      - ./data:/var/lib/mysql

  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    container_name: phpmyadmin
    restart: always
    environment:
      PMA_HOST: db
      MYSQL_ROOT_PASSWORD: "Ваш пароль"
    ports:
      - "Ваш порт:80"

volumes:
  data:

Схема бд находится в Файле database/models.py
Как накатить миграцию, можно найти в интернете. Скрипт по миграции я не писал.
## Установка проекта:
1. git clone https://github.com/Jagernau/bitrix_work
2. Создать виртуальное окружение в папке bitrix_work
3. pip install -r requirements.txt
Прописать зависимости в .env Подсмотреть какие нужны можно в файле конфигурирования: configurations/config.py
4. Накатить миграцию либо воспользоваться бэкапом схемы бд(в дальнейшем я её выложу)
5. Написать юнит Systemd для запуска сбора данных, на файл main.py.

## Для полноценной функциональности:
1. Воспользуйтесь cms на django: https://github.com/Jagernau/django_work
2. 



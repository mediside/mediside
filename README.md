# Описание

Сборка и запуск WEB-сервиса для распознавания патологий на снимках КТ.

# Клонирование проекта

Клонирование с вытягиванием всех подмодулей:

```bash
git clone --recurse-submodules git@github.com:mediside/deploy.git hackathon
cd hackathon
```

> Адреса подмодулей указаны для SSH. Вам нужно добавить ключ SSH в профиле GitHub. 

# Разработка
```bash
docker compose -f docker-compose-dev.yaml up # запуск
docker copmose -f docker-compose-dev.yaml down # остановка и удаление
```

# Деплой

```bash
docker compose -f docker-compose-prod.yaml up -d # запуск
docker copmose -f docker-compose-prod.yaml down # остановка и удаление
```

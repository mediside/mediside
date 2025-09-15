# Описание

Сборка и запуск WEB-сервиса для распознавания патологий на снимках КТ.

# Клонирование проекта

Клонирование с вытягиванием всех подмодулей:

```bash
git clone --recurse-submodules git@github.com:mediside/deploy.git hackathon
cd hackathon
```

> Адреса подмодулей указаны для SSH. Вам нужно добавить ключ SSH в профиле GitHub. 

# Использование

```bash
docker compose up -d # запуск
docker copmose down # остановка и удаление
```

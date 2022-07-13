![Foodgram](https://github.com/makeitokay/foodgram-project/workflows/Foodgram%20Main%20Workflow/badge.svg)

# Продуктовый помощник Foodgram

Foodgram - это сервис для настоящих кулинаров и гурманов! Здесь вы можете:
- Просматривать рецепты, созданные другими людьми
- Создавать собственные рецепты
- Подписываться на любимых авторов
- Добавлять лучшие рецепты в избранное
- Составлять свой список покупок ингредиентов для рецептов блюд, которые вы хотите приготовить
- Удобно фильтровать список рецептов по тэгам: завтрак, обед и ужин

Попробовать можно здесь: https://makeitokay.pythonanywhere.com/

# Техническая часть проекта

Проект написан с использованием веб-фреймворка Django и Django Rest Framework.
Запущен с помощью Gunicorn, используется база данных PostgreSQL, настроен nginx.
И, конечно же, завернут в Docker контейнеры! ([ссылка на Docker Hub](https://hub.docker.com/r/makeitokay/foodgram))

## Как запустить?

Всё просто - для этого на вашей машине понадобится установленный [Docker](https://docs.docker.com/engine/install/) и [docker-compose](https://docs.docker.com/compose/install/).
- Склонируйте этот репозиторий
- В папке /foodgram-project/foodgram/ выполните команду ```docker-compose up --build```
- После того, как контейнеры будут запущены, необходимо выполнить миграции и собрать статику:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
```
Проект запущен локально и доступен по адресу http://localhost!

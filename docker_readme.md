    sudo docker compose down
    sudo docker compose build
    sudo docker compose up -d
    sudo docker ps -a
    
    sudo docker logs --tail 100 kmv_2-app-1
    sudo docker logs --tail 100 kmv_2-db-1
    sudo docker logs --tail 100 kmv_2-web-1

    
    sudo docker-compose logs -f

---
Удалит тома вместе с контейнерами:

    docker-compose down -v
---
Запустить миграцию:

    $ docker-compose exec web python manage.py migrate --noinput
---
Создайте суперпользователя командой:

    $ docker-compose exec web python manage.py createsuperuser 
---





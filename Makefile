build:
	docker build -t routing-web-image .

run:
	docker run -d --name routing-web-app -p 8000:8000 routing-web-image

stop:
	docker stop routing-web-app

start:
	docker start routing-web-app

up:
	docker compose up --build -d

down:
	docker compose down

restart:
	docker compose restart

pull:
	git pull

logs:
	docker logs routing-web-app

prune:
	docker system prune -a --volumes -f

shell:
	docker exec -it routing-web-app /bin/sh

migrate:
	docker exec routing-web-app python manage.py makemigrations && python manage.py migrate

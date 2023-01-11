containers:
	docker-compose up

main-containers:
	cd composes/main; docker-compose up

down-main-containers:
	cd composes/main; docker-compose down

main-containers-d:
	cd composes/main; docker-compose up -d

bg-containers:
	cd composes/tasks && docker-compose up

bg-containers-d:
	cd composes/tasks && docker-compose up -d
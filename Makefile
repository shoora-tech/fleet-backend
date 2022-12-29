containers:
	docker-compose up

main-containers:
	cd composes/main; docker-compose up

bg-containers:
	cd composes/tasks && docker-compose up
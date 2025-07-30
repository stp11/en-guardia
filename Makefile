generate-client:
	cd frontend && bun run generate-client

start-frontend:
	cd frontend && bun run dev

start-backend:
	docker-compose up -d

lint-frontend:
	cd frontend && bun run prettier:fix && bun run lint:staged

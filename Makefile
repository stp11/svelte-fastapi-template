setup:
	[ -f backend/.env ] || cp backend/.env.example backend/.env
	[ -f frontend/.env ] || cp frontend/.env.example frontend/.env
	cd frontend && bun install

generate-client:
	cd frontend && bun run generate-client

start-frontend:
	cd frontend && bun run dev

start-backend:
	docker compose up -d

# Volumes are kept, so the database survives.
stop-backend:
	docker compose down

test-backend:
	docker compose exec backend python -m pytest

# make migration m="add something"
migration:
	docker compose exec backend alembic revision --autogenerate -m "$(m)"

lint-frontend:
	cd frontend && bun run prettier:fix && bun run lint:staged

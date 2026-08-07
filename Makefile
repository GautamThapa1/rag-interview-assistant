.PHONY: dev qdrant-init qdrant-start qdrant-stop redis-init redis-start redis-stop

# Run the FastAPI development server with auto-reload
dev:
	uv run uvicorn app.main:app --reload

# Create a Qdrant container with persistent storage (run once)
qdrant-init:
	docker run -d \
		--name qdrant \
		-p 6333:6333 \
		-v qdrant_data:/qdrant/storage \
		qdrant/qdrant

# Start the existing Qdrant container
qdrant-start:
	docker start qdrant

# Stop the Qdrant container
qdrant-stop:
	docker stop qdrant

# Create a Redis container (run once)
redis-init:
	docker run -d \
		--name redis \
		-p 6379:6379 \
		redis

# Start the existing Redis container
redis-start:
	docker start redis

# Stop the Redis container
redis-stop:
	docker stop redis
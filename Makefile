.PHONY: dev qdrant

dev:
	uv run uvicorn app.main:app --reload

# docker run -d \
#   --name qdrant \
#   -p 6333:6333 \
#   -v qdrant_data:/qdrant/storage \
#   qdrant/qdrant

# docker stop qdrant
# docker start qdrant

# docker run -d --name redis -p 6379:6379 redis

# docker stop redis
# docker start redis
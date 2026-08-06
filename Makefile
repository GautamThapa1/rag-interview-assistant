.PHONY: dev qdrant

dev:
	uv run uvicorn app.main:app --reload

qdrant:
	docker run -p 6333:6333 qdrant/qdrant
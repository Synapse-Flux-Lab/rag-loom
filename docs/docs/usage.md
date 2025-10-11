---
id: usage
title: Usage Guide
sidebar_position: 3
---

## Start the Service

`docker build -t rag-microservice .`
`docker run -p 8000:8000 rag-microservice`

or
activate venv,
install dependencies,
`python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`

## Upload a Document

`curl -X POST "http://localhost:8000/api/v1/ingest" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf" \
  -F 'chunk_params={"chunk_size": 1000, "chunk_overlap": 200}'
  `

## Ingest a Document

`curl -X POST "http://localhost:8000/api/v1/ingest" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
`

## Search for Similar Content

`curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is machine learning?",
    "top_k": 5,
    "similarity_threshold": 0.7
  }'`

## Generate an Answer

`curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is machine learning?",
    "search_params": {
      "top_k": 5,
      "similarity_threshold": 0.7
    },
    "temperature": 0.7,
    "max_tokens": 500
  }'`

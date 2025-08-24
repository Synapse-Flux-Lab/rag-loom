# start service

`docker build -t rag-microservice .`
`docker run -p 8000:8000 rag-microservice`


# Upload a document

`curl -X POST "http://localhost:8000/api/v1/ingest" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf" \
  -F 'chunk_params={"chunk_size": 1000, "chunk_overlap": 200}'
  `
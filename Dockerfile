# FROM python
FROM python:3.9-alpine

RUN mkdir /service
WORKDIR /service
ENV PYTHONPATH=/service
ENV GRPC_VERBOSITY=debug
RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk add build-base
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 23335
COPY . .
WORKDIR /service
ENTRYPOINT [ "python", "hybrid_server.py"]

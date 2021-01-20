FROM python:3.7-alpine

RUN apk add --update  --no-cache libstdc++ libc6-compat openssh-client git gcc cython linux-headers make musl-dev python3-dev g++
ENV GRPC_PYTHON_VERSION 1.15.0
RUN pip install grpcio==${GRPC_PYTHON_VERSION} grpcio-tools==${GRPC_PYTHON_VERSION}


EXPOSE 8090

CMD [ "python", "./main.py" ]
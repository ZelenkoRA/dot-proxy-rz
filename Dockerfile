FROM python:3.8.2-alpine3.10

WORKDIR /usr/local/bin
COPY proxy.py .

EXPOSE 53/tcp

CMD ["python","-u","proxy.py"]

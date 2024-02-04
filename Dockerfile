from python:3.10.11
expose 5000
RUN apt-get update && \
    apt-get install -y gcc make apt-transport-https ca-certificates build-essential
CMD mkdir -p /app
WORKDIR /app
copy requirements.txt ./requirements.txt
run pip install -r requirements.txt
copy . .
RUN ls ./
ENV FLASK_APP=app
CMD ["python","app.py"]

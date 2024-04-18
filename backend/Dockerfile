FROM python:3.11

# Install postgresql-client
RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /usr/src/app

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY . .

EXPOSE 80

COPY scripts/wait-for-postgres.sh /wait-for-postgres.sh
RUN chmod +x /wait-for-postgres.sh

CMD /wait-for-postgres.sh uvicorn app.main:app --host 0.0.0.0 --port 80

Generate secret key

```shell
openssl rand -hex 32
```

Populate database with dummy user data

```shell
docker-compose exec backend python utils/seed_db.py
```

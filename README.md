# En Guàrdia

App en honor al programa [En Guàrdia!](https://www.3cat.cat/3cat/en-guardia/) de Catalunya Ràdio.

## Backend

`docker-compose up --build -d`

Per popular la base de dades

`python -m commands.ingest_data`

### Base de dades

Si fas canvis a la base de dades executa, crea una migració:

`alembic revision --autogenerate -m "Nom de la migració"`

I després, per reflectir els canvis:

`alembic upgrade head`

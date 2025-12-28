# En Guàrdia

Arxiu **no oficial** del programa
[En Guàrdia!](https://www.3cat.cat/3cat/en-guardia/)
de **Catalunya Ràdio**.

Aquest projecte organitza i indexa informació pública del programa
per facilitar la cerca, la navegació i el filtratge mitjançant una
interfície alternativa.

**Projecte independent**
Aquest projecte **no està afiliat ni avalat** per Catalunya Ràdio
ni per la Corporació Catalana de Mitjans Audiovisuals (CCMA).

---

## Backend

Per iniciar els serveis:

```bash
docker-compose up --build -d
```

Per popular la base de dades amb dades obtingudes dels endpoints públics:

```bash
python -m commands.ingest_data
```

Per classificar els episodis afegeix la teva OPENAI_API_KEY i executa:

```bash
python -m command.classify_episodes --batch_size={batch_size} --max_total={max_total}
```

## Base de dades

Si fas canvis en els models, crea una migració:

```
alembic revision --autogenerate -m "Nom de la migració"
```

Aplica-la amb:

```
alembic upgrade head
```

## Frontend

Aplicació desenvolupada amb **SvelteKit** configurada com a SPA (Single Page Application).

### Scripts

Instal·lar dependències:

```bash
cd frontend
bun install
```

Iniciar el servidor de desenvolupament:

```bash
bun run dev
```

Generar el client de l'API (després de canvis al backend):

```bash
bun run generate-client
```

Compilar per producció:

```bash
bun run build
```

---

# Avís legal

El codi font d’aquest projecte està publicat sota la llicència MIT.

Aquesta llicència s’aplica exclusivament al codi i no concedeix cap dret
sobre continguts de tercers.

Tots els drets sobre els podcasts, àudios, textos, marques i materials
relacionats amb En Guàrdia! pertanyen als seus respectius titulars.

L’ús d’aquest programari és responsabilitat de l’usuari final, que ha
d’assegurar-se de complir la normativa i condicions aplicables.

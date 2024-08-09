
The database is stored inside a volume. Volumes are used in Docker to persist data, 
ensuring that the data remains intact even if the container is stopped or removed.

When you specify a volume in your docker-compose.yml file, Docker creates a volume 
on the host machine to store the data. This volume is then mounted into the container 
at a specified path. This ensures that the data is persisted across container restarts.

In your docker-compose.yml file, you have specified volumes for the PostgreSQL containers. 
```
services:
  user_db:
    image: postgres:13
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: user_db
    volumes:
      - user_db_data:/var/lib/postgresql/data
```

Inspecting the Volume:<p>
List Docker Volumes: `docker volume ls`.
This will show a list of all Docker volumes. You should see user_db_data and product_db_data in the list.

Inspect a Specific Volume:<p>
`docker volume inspect user_db_data`
This will provide detailed information about the volume, including the mount point on the host machine.


The database tables are mounted and managed within the user_db container. The user_db container is running the PostgreSQL database server, and it uses a Docker volume to persist its data. The user_service container, on the other hand, connects to the user_db container to interact with the database but does not manage the database files directly.

Summary of Container Roles
user_db Container:

Runs the PostgreSQL database server.
Manages and stores the database tables.
Uses a Docker volume (user_db_data) to persist the database data.
user_service Container:

Runs the Flask application.
Connects to the PostgreSQL database running in the user_db container to perform database operations (CRUD operations) via SQLAlchemy.

```
docker volume inspect user_db_data
```

```
docker-compose exec user_db bash
ls /var/lib/postgresql/data

#connect to DB
psql -U user -d user_db

# List all tables
\dt

# Exit the PostgreSQL prompt
\q

# Exit the container
exit
```

Restarting a container:
```
docker-compose restart user_service
```
If you need to rebuild the image or ensure the service is fully recreated, 
you can use the up command with the --force-recreate option:
```
docker-compose up --force-recreate user_service
```

Execute migrations for a table:
```
docker-compose exec user_service flask db init
docker-compose exec user_service flask db migrate -m "Initial migration."
docker-compose exec user_service flask db upgrade
```

For V2, it's `docker compose` without a hyphen
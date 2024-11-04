FROM postgres:16-alpine
ENV POSTGRES_PASSWORD=secret
ENV POSTGRES_USER=username
ENV POSTGRES_DB=lines_database
COPY lines_database.sql /docker-entrypoint-initdb.d/lines_database.sql

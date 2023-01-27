# Deploy on your pc

1. Download [PostgreSQL](https://www.postgresql.org/) (if you don't have it)
2. create an .env file in the root of the project
3. In it you must add the following fields and fill it in with your data
```
    DB_HOST=your_host
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_PORT=5432 # It is the default Postgres port, you can change it if your configuration is different
```
4. Run ```python app.py```

## API Server

Initiate API server

```
cd backend
uvicorn app.main:app --reload
```

## Postgres Database

Configurations

```
Server Name       = dev
Host Name/Address = localhost
Port              = 5432
Database          = postgres/taskz
User              = postgres
Password          = Admin@123
```

Change working directory

```
cd C:\Users\bhoopesh.sharma\AppData\Local\Programs\pgsql\bin
```

Start postgres server

```
pg_ctl -D ../data -l ../logfile start
```

Stop postgres server 

```
pg_ctl -D ../data stop
```
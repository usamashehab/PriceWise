# PriceWise

## Installation

To install and run this project locally, follow these steps:

1. Clone the repository:

```bash
$ git clone https://github.com/usamashehab/PriceWise.git
```

2. Change into the project directory:

```bash
$ cd PriceWise
```

3. Install the required dependencies:

```bash
$ pip install -r requirements.txt
```

4. create a PostgreSQL database called pricewise for user postgres and add the pg_trgm extension:
   pg_trgm is responisble for enabling fulltext search

   1-First, make sure you have PostgreSQL installed and running on your system.

   2-Open a terminal or command prompt and log in to the postgres user:

   for linux:

   ```bash
   sudo -u postgres psql
   CREATE DATABASE pricewise;
   \c <DB_NAME>;
   CREATE EXTENSION pg_trgm;
   ```

   for windows:

   ```bash
   psql
   ```

   enter you credintals then:

   ```bash
   CREATE DATABASE pricewise;
   \c <DB_NAME>;
   CREATE EXTENSION pg_trgm;
   ```

5. migrate the database

```bash
$ python manage.py migrate
```

5. Start the development server:

```bash
$ python manage.py runserver
```

6. Open a web browser and navigate to `http://localhost:8000/redoc/` to access the APIs documentation.

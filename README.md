# file_system
***
1. I was unable to create a CLI for webpage so frontend won't work. However, backend is fully operational. To test, use POSTMAN to make call to ```http://127.0.0.1:8000/``` with appropriate request according to [link](https://docs.google.com/document/d/1fG_gXxn6YWU54vWo3KuIHg9FzdicbvA-nzNCzVuMgYA/edit?usp=sharing) after sunning backend.
***

# file system backend

1. Install postgreSQL from https://www.postgresql.org/download/

2. Add `PostgreSQL/[version, either 12 or 13]/bin` and `PostgreSQL/[version, either 12 or 13]/lib` to PATH (on Windows) or make it an environment variable on Mac/Linux.

- To make environment variable use the following command
```
export POSTGRES_HOME=/Applications/Postgres.app/Contents/Versions/latest
export PATH=$POSTGRES_HOME/bin:$PATH
```

- Confirm installation
```
psql --version
```

3. Setup your local POSTGRES database.
- You can use the following to guide on how you can setup your local POSTGRES DV: https://medium.com/@rudipy/how-to-connecting-postgresql-with-a-django-application-f479dc949a11 

4. Connect local POSTGRES database to Django application.
- Navigate to `./file_system_backend/file_system_backend/` directory and add a .env file with the following environment variables:
![environment variables](./img/environment_variables.png)

5. Install dependencies.
- Navigate to `./file_system_backend/` directory and run the following command
```
pip install -r requirements.txt
```

6. Apply migrations to your local DB.
- Navigate to `./simulator_backend/ directory` and run the following command:
```
python manage.py migrate
```

7. Run server.
```
python manage.py runserver
```

8. You can now interact with our API by making the appropriate API calls.
- Checkout this [link](https://docs.google.com/document/d/1fG_gXxn6YWU54vWo3KuIHg9FzdicbvA-nzNCzVuMgYA/edit?usp=sharing) for API documentation.

# If you run into errors with Postgres, it will be helpful to drop the Postgres database and start from scratch:
1. Login as a postgres superuser with the following command and type in the superuser's password(created when you first installed Postgres) when prompted.
```
psql --u postgres
```

2. Drop simulator_backend database and create it again.
```
DROP DATABASE <database name>;
CREATE DATABASE <database name>;
```

3. Grant all privileges to your postgres user.
```
GRANT ALL PRIVILEGES ON DATABASE <database name> TO <username>;
```

4. Exit postgres command line.
```
\q
```

5. Continue from Step 6 above(Apply migrations to your local DB).

# file system frontend

0. Make sure backend is running

# file system CLI syntax:
***
All path must be absolute path to folder/file and must end with '/' in the end.
For instance:
- a valid path for FOLDER is <root/> for folder name 'root or <root/folder/> for folder name 'folder' inside 'root' folder.
- a valid path for FILE is <root/file/> for file name 'file' in 'root' folder
***

1. create filde/folder
- format: ```cr [PATH] [DATA]```
- [PATH] is required but [DATA] is optional. If [DATA] is provided, server will create a file, otherwise, server will create a folder.
- example:
    - for folder: cr root_folder/
    - for file: cr root/file/ this is a file

2. cat file
- format: ```cat [FIlE PATH]```
- [FILE PATH] is required.
- example:
    - cat root/file/

3. list folder
- format: ```list [FOLDER PATH]```
- [FOLDER PATH] is required.
- example:
    - list root/

4. move folder/file
- format: ```mv [PATH] [NEW DIRECTORY PATH]```
- [PATH] and [NEW DIRECTORY PATH] are required.
- example:
    - moving folder to folder_1: mv root/folder/ root/folder_1/

5. remove folder/file
- format: ```rm [PATH]```
- [PATH] is required.
- example:
    - rm root/folder/

5. update folder/file
- format: ```up [PATH] [NEW NAME] [DATA]```
- [DATA] is optional but [PATH] and [NEW NAME] are required. If [DATA] is provided, server will update a file, otherwise, server will update a folder or file depends on the [PATH].
- example:
    - for file with no new data: up root/file/ file_new
    - for file with new data: up root/file/ file_new this is a test for move
    - for folder: up root/folder/ folder_new
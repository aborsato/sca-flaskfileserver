# Flask File Server
Sample file server that checks user credentials in a Database. Written in Python/Flask.

## Set Up
Clone (or download) this repo and create a virtual environment.
```bash
python3 -m venv .venv
```

Activate the environment and install the dependencies.
```bash
source ./.venv/bin/activate
pip install -r requirements.txt
```

The sqlite3 (`database.sqlite3`) database has 2 entries. The application look up this table before proceeding with the download, so it will accept downloads for these two files only:
```
sqlite> select * from metadata;
1|OLDFILE|charlie|2020-01-01 10:00:00
2|NEWFILE|alice|2021-10-01 10:00:00
```
The `OLDFILE` file has an `uoloaded_date` set to more than one year in the past to test the logic that bypasses the owner for old files. The ``

## Run

You can start the server by running:
```bash
python main.py
```

Open the URL in you browser:
|URL|Effect|
|--|--|
|`curl http://127.0.0.1:5000/download/OLDFILE`|It downloads the file, because the `uploaded_date` is past 1 year.|
|`curl http://127.0.0.1:5000/download/NEWFILE`|It will return HTTP code 404 (not found), because the `uploaded_date` is less then 1 year and there is no user.|
|`curl http://127.0.0.1:5000/download/NEWFILE -H "user: bob"`|It will return HTTP code 404 (not found), because `bob` is not the owner.|
|`curl http://127.0.0.1:5000/download/NEWFILE -H "user: alice"`|It downloads the file, because `alice` is the owner.|
|`curl http://127.0.0.1:5000/download/NEWFILE --cookie "user=alice"`|It downloads the file, cookie is also accepted as parameter.|

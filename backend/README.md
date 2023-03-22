# Backend (API) part of the sol-db-in

The website is working as a React App, so the backend python server
provides only an API to the database and export logic

## Installation and setup

0. You should have python `3.10`
1. Clone the repository:\
`git clone https://github.com/KennelTeam/sol-db-in`
2. Install python libraries:\
`pip install -r backend/requirements.txt`
3. Provide a `.env` file in the root folder. 
This `.env` file should have fields as in `example.env`
4. Check the `config.json` and make sure that server is 
configured as you want it to be
5. Run: `make run`

To run project code checks activate a python 3.10 venv with all libraries 
from `requests.txt` installed. And call `make all_checks`.

## Project structure

- `__main.py__` - the file that will run
- `.pylintrc` and `pytype.config` are checkers config files
- `constants.py` - all the public configuration of server is stored here
- `auxiliary/` - folder with auxiliary types, functions and classes
- `app/` - folder with flask app
  - `app/api/` - folder to store API requests processors. You can read 
further about API internal structure in [API readme](app/api/README.md)
  - `app/database/` - folder to store DB connection processors
and DB ORM classes. You can read further about database architecture 
in [database readme](app/database/README.md)

## The FlaskApp singleton object

There is a class `FlaskApp` in the `backend.app` module.
It contains all the flask items (app object, api object, db object).
`FlaskApp` is a singleton, with readonly properties `app`, `api` and `db`.
`FlaskApp().init_database()` initializes the database 
(creates missing tables and so on...)

`FlaskApp().request(Table)` is similar to usual sqlalchemy
`Table.query`, but if needed the `request` function filters only non-deleted
items from the database.

`run_dev_server` and `run_prod_server` start a flask server app

`use_deleted_items_in_this_request` changes flask `app_context`
so that during processing of this request deleted items will also be included
in the respone.

`add_database_item(item)` adds item to the local cache (not saves to the DB)

`flush_to_database()` saves all cached changes
(creations, updates and deletions) to the database
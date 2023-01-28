# Backend (API) part of the sol-db-in

The website is working as a React App, so the backend python server
provides only an API to the database and export logic

## Installation and setup

1. Clone the repository:\
`git clone https://github.com/KennelTeam/sol-db-in`
2. Install python libraries:\
`pip install -r backend/requirements.txt`
3. Provide a `.env` file in the `backend` folder. 
This `.env` file should have fields as in `example.env`
4. Check the `config.json` and make sure that server is 
configured as you want it to be
5. Run the `backend` module with python 3.8:\
`python3 -m backend` on linux\
`python -m backend` on windows

## Project structure

- `__main.py__` - the file that will run
- `config.json` - all the public configuration of server is stored there
- `app/` - folder with flask app
  - `app/api/` - folred to store API requests processors
  - `app/database/` - folder to store DB connection processors
and DB ORM classes. You can read further about database architecture 
in [database readme](app/database/README.md)

# Mastermind

Flask backend server for the Mastermind game to handle code generation and verify guesses. 

## Running the Flask Server Locally

### Create virtual environment

Navigate to the project directory (`cd mastermind`):

```bash
## create a virtual environment
python3 -m venv venv

## activate virtual environment
source venv/bin/activate 

## install packages
pip install -r requirements.txt

## when deactivating virtual environment: 
deactivate

## Create Databases

PostgreSQL was used for the database in this project.

```bash
createdb mastermind

Create a .env file to connect to the database. In the mastermind folder, enter the following:
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/mastermind

Depending on what port is used, 5432 may be a different number.
If you name the database something other than mastermind, then mastermind should be changed to the database name!


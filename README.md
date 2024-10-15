# Mastermind Backend Server

The backend system for Mastermind, a code breaking game. It provides a RESTful API for creating, reading, updating, and deleting (CRUD) resources required to play the game. Built with Flask and PostgreSQL. The backend server is being utilized to support the Mastermind site.

**Check out the Website: [Mastermind](https://valerie-valentine.github.io/mastermin-frontend)**

## Getting Started

### Prerequisites

- flask
- flask-sqlalchemy
- flask-migrate
- flask-bcrypt
- flask-cors
- python-dotenv
- psycopg2-binary
- pytest

## Running the Flask Server Locally

### Create virtual environment

Navigate to the project directory (`cd mastermind`):

#### Create a virtual environment

```bash
python3 -m venv venv
```

### Install packages

```bash
pip install -r requirements.txt
```

## When deactivating virtual environment:

```bash
deactivate
```

### Create Databases

PostgreSQL was used for the database in this project.

```bash
createdb mastermind
```

.env file to connect to database

Create a .env file in the mastermind folder and enter the following:

```bash
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/mastermind
```
- Depending on what port is used, 5432 may be a different number

Run Flask Server
Apply migrations to database:

```bash
flask db upgrade
```

Navigate to project folder (mastermind):

```
bash
flask run
```

### Tests

Tests can be run using the command pytest tests/test_routes.py from the mastermind folder.

### MVP

I began with a command line script for this game in order to break down the logic and functionality required to implement a minimum viable product. Narrowing my initial scope to just focusing on how to calculate the number of correct digits and location in the guess, generate a random number, as well as input validation and error handling. Once I was able to establish the logic, I wanted to create a companion site to serve as a visual for the game. Initially, I just wanted the user to be able to play a game against the computer. Once that was established, I was able to then focus on the additional features: i.e. login, user profile, account creation and deletion.
Additional Features

    Customizable difficulty levels:
        Easy (4 digit code)
        Medium (6 digit codes)
        Hard (8 digit code)
    Users are able to choose from what range they would like the numbers to be generated from (i.e: 0-4 -> 0404)
    Users are able to customize how many lives may be played (no less than 3 or more than 20)
    Option to login/create a user profile that can save the games played and allow you to continue unfinished games, and view your past games data
    Ability to see previous guesses, instructions and feedback of guess
    Leaderboard that displays the top 10 players based off of most games won
    Ability for a user to delete a game or user account
    Ability to store and retrieve hashed passwords
    Generate a hint for user

### Backend Design & Considerations

I utilized PostgreSQL, Flask and SQLAlchemy for the backend of this project because it seemed to be a relatively lightweight application. The backend for mastermind consists of 3 tables: Games, Guesses, and Clients. The core logic I focused on implementing was being able to generate a game, guess, user and check a guess against an answer. After achieving these tasks, I really wanted to incorporate different ways to make this game customizable. This included allowing users to customize the start settings for a game, ability for users to create an account and view history of games, choosing the length of the code and what type of digits it will be. With these extensions particularly, persisting user information, really required me to research about authentication and authorization principles. I initially used username and password to authenticate a user, but refactored the application to utilize password hashing to handle security around passing sensitive information. Additionally, I created a third field "email" to use along authentication with the hashed password. This allowed me to then display user's display handles (this case username) where needed visibly while keeping their email hidden.
Models

    Game Model (Game Table):
        Stores information about the game (lives, difficulty_level, answer), as well as what parameters were utilized in the generation of the answer (num_min, num_max)
        Games have a one to many relationship with guesses, with guesses having to be associated with a game.
        Users have a one to many relationship with Games. To support the greatest flexibility though, games do not have to be associated with a user (can have the foreign key be None)
    Guess Model (Guess Table):
        Stores information about guesses for the game, including the guess value, how many correct digits are included and how many are in the correct location
        Each guess is associated with a game and cannot be added to the database without an existing relationship to a game
    User Model (User Table):
        I wanted to add a way for users to see their game history, see what games they've won/lost, and also be able to continue unfinished games
        Created a user model that stores a user's username, email, password, score, and their games

### Routes

The routes folder consists of the API endpoints, with routes_helper consisting of helper functions for input validation and external API calls to the random number generator.
Client Routes:

    - Endpoints support creating a user
    - Logging in a user (validating that user exists, username and password are correct)
    - Getting a user's information
    - All the games belonging to a user
    - Deleting a user's account
    - Getting the top users for the game

Games Routes:

    - Endpoints for creating a game
    - Creating a guess (guess must be associated with a game)
    - Getting a game from a game_id
    - Getting all guesses for a game from the game_id
    - Getting a hint based off of last guess made for a game
    - Deleting a game from the user's account
    - Getting all games for the application



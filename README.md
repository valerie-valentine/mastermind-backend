# Mastermind Backend Server 2.0

The backend system for Mastermind, a code breaking game. It provides a RESTful API for creating, reading, updating, and deleting (CRUD) resources required to play the game. Built with React, Flask, and PostgreSQL. The backend server is being utilized to support the Mastermind site.

**Check out the Website: Deployment coming soon!**

### Features/ Extensions  

- **Customizable Difficulty Levels**: Easy (4 digits), Medium (6 digits), Hard (8 digits)  
- **Custom Range**: Set number range for code generation (e.g., `0-4` → `0404`)  
- **Custom Lives**: Choose between 3 to 20 lives  
- **User Profiles**: Save games, continue unfinished games, view past game data  
- **Gameplay Tools**: Track previous guesses, generate hints, view instructions  
- **Leaderboard**: Top 10 players by games won  
- **Account Management**: Delete user accounts or specific games  
- **Security**: Passwords stored with hashing  


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
CREATE DATABASE my_database_name;
```

.env file to connect to database

Create a .env file in the mastermind folder and enter the following:

```bash
SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/mastermind
```
- Depending on what port is used, 5432 may be a different number

### Initialize database & run Flask server

Intialize database:
```bash
flask db init
```

Create a migration:
```bash
flask db migrate -m "Initial migration"
```

Apply migrations:

```bash
flask db upgrade
```

Navigate to project folder (mastermind):

```bash
flask run
```

### Tests

Tests can be run using the command pytest tests/test_routes.py from the mastermind folder.

### Backend Design & Considerations

While revisiting this project for a second iteration, my primary focus was on refactoring with an emphasis on code organization, encapsulation, and separation of concerns. In the initial implementation, many of my helper functions were consolidated into a single, bloated file. To improve maintainability, I refactored the code by introducing a helpers module and distributing the functions into individual files based on their respective responsibilities. For example:

    - helpers/validation.py contains all validation-related helper functions.
    - helpers/random_utils.py handles network calls for generating random numbers.
    - helpers/module_helpers.py includes reusable module-specific functionality.

Additionally, I encapsulated shared functionality by integrating related helper methods into their respective classes as instance methods. For instance, in the Game model, I added methods such as generate_hint and check_status, which encapsulate game logic and update the model's attributes as needed.

Since my previous work on this project, I also updated the implementation to reflect new practices in Flask and SQLAlchemy. Models now utilize Python type hinting, and the previously used query class member has been deprecated. I adopted the preferred approach of building queries using SQL-like functions and executing them with db.session. Similarly, newer Flask versions no longer require explicitly "jsonifying" lists, so I streamlined my route responses to directly return dictionaries and lists.

To maintain consistency and scalability, I aimed to follow the MVC design pattern. In my console-based application, the MVC pattern naturally aligned with the structure. However, in the backend version, this structure felt somewhat redundant. The existing architecture already adhered to MVC principles, with the database serving as the model, the routes acting as controllers, and the React frontend as the view layer (itself an MVC application). In a separate branch (mastermind-backend-2.0), I experimented with additional abstraction by creating client_controllers and game_controllers. While this provided theoretical flexibility for expanding database logic in the future, it ultimately felt redundant and resembled middleware functions without significant added value. I reverted to a simpler, route-driven approach while keeping this abstraction in mind for future scalability.

I've also included error handling for my random_number_api function to address potential issues such as API failures, network interruptions, or service unavailability.
  

## Challenges and Lessons Learned

Refactoring introduced several challenges, particularly around breaking changes in models and routes. Debugging these issues required careful planning and a structured workflow. I used feature branches to experiment with changes and tracked the most stable version of the application. Incremental refactoring, paired with testing the backend in conjunction with the frontend, allowed me to identify and resolve bugs efficiently. This experience taught me the importance of a systematic approach to refactoring, thorough testing, and maintaining a stable workflow throughout the process.

### Future Updates
I would like to extend to realtime multi-player and include a timer that visually displays.

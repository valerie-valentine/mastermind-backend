# Mastermind Backend Server 2.0

The backend system for Mastermind, a code breaking game. It provides a RESTful API for creating, reading, updating, and deleting (CRUD) resources required to play the game. Built with React, Flask, and PostgreSQL. The backend server is being utilized to support the Mastermind site.

**Check out the Website: Deployment coming soon!**

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

### Backend Design & Considerations

While revisiting this project for a second iteration, my primary focus was on refactoring with an emphasis on code organization, encapsulation, and separation of concerns. In the initial implementation, many of my helper functions were consolidated into a single, bloated file. To improve maintainability, I refactored the code by introducing a helpers module and distributing the functions into individual files based on their respective responsibilities. For example:

    - helpers/validation.py contains all validation-related helper functions.
    - helpers/random_utils.py handles network calls for generating random numbers.
    - helpers/module_helpers.py includes reusable module-specific functionality.

Additionally, I encapsulated shared functionality by integrating related helper methods into their respective classes as instance methods. For instance, in the Game model, I added methods such as generate_hint and check_status, which encapsulate game logic and update the model's attributes as needed.

Since my previous work on this project, I also updated the implementation to reflect new practices in Flask and SQLAlchemy. Models now utilize Python type hinting, and the previously used query class member has been deprecated. I adopted the preferred approach of building queries using SQL-like functions and executing them with db.session. Similarly, newer Flask versions no longer require explicitly "jsonifying" lists, so I streamlined my route responses to directly return dictionaries and lists.

To maintain consistency and scalability, I aimed to follow the MVC design pattern. In my console-based application, the MVC pattern naturally aligned with the structure. However, in the backend version, this structure felt somewhat redundant. The existing architecture already adhered to MVC principles, with the database serving as the model, the routes acting as controllers, and the React frontend as the view layer (itself an MVC application). In a separate branch (mastermind-backend-2.0), I experimented with additional abstraction by creating client_controllers and game_controllers. While this provided theoretical flexibility for expanding database logic in the future, it ultimately felt redundant and resembled middleware functions without significant added value. I reverted to a simpler, route-driven approach while keeping this abstraction in mind for future scalability.

I've also included error handling for my random_number_api function to address potential issues such as API failures, network interruptions, or service unavailability.

### Extensions:

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

## Challenges and Lessons Learned

Refactoring introduced several challenges, particularly around breaking changes in models and routes. Debugging these issues required careful planning and a structured workflow. I used feature branches to experiment with changes and tracked the most stable version of the application. Incremental refactoring, paired with testing the backend in conjunction with the frontend, allowed me to identify and resolve bugs efficiently. This experience taught me the importance of a systematic approach to refactoring, thorough testing, and maintaining a stable workflow throughout the process.


While revisiting this project for a second iteration, my primary focus was on refactoring with an emphasis on code organization, encapsulation, and separation of concerns. In my initial implementation, many of my helper functions were consolidated into a single file, resulting in bloated and difficult-to-maintain code. To address this, I refactored the codebase by introducing a modular structure, distributing helper functions into individual files based on their specific responsibilities.

For example:

    helpers/validation.py: Contains all validation-related helper functions, ensuring a single point of truth for form or input validation logic.
    helpers/random_utils.py: Handles the network call for generating random numbers, isolating external dependencies from core logic.
    helpers/module_helpers.py: Includes reusable utility functions to streamline and centralize shared module-specific functionality.

This modular approach not only improved code readability and maintainability but also made testing and debugging significantly easier.

Additionally, I refactored shared functionality by integrating helper methods directly into their corresponding classes as instance methods. This encapsulation ensured that functionality was logically grouped within the relevant domain. For instance, in the Game model, I implemented methods such as generate_hint and check_status. These methods encapsulate core game logic, making it easier to update attributes and maintain consistency across the application.
Adopting Updated Framework Practices

Since my previous work on this project, newer versions of Flask and SQLAlchemy introduced updates that influenced my refactoring process:

    SQLAlchemy Model Updates: I updated my models to utilize Python type hinting, which enhances code clarity and assists with static analysis tools. The deprecated query class member was replaced with SQL-like query-building methods, executed via db.session. This adjustment aligns the codebase with modern standards and facilitates better maintainability in future iterations.
    Flask Route Optimization: Flask's newer versions no longer require "jsonifying" lists explicitly. I updated my route handlers to return dictionaries and lists directly, leading to cleaner and more concise code.

Applying the MVC Design Pattern

To maintain a scalable and well-structured architecture, I followed the Model-View-Controller (MVC) design pattern throughout the project. This approach naturally aligned with the structure of my console-based application. However, in the backend version, it initially felt redundant. The architecture already included:

    Model: Represented by the database and SQLAlchemy models.
    Controller: Managed by the Flask route handlers.
    View: Handled by the React frontend, which operates as a standalone MVC application.

To explore further abstraction, I experimented in a separate branch (mastermind-backend-2.0) by creating client_controllers and game_controllers modules. While this additional layer offered theoretical flexibility for managing more complex database logic, it often felt unnecessary and resembled middleware rather than true abstraction. Ultimately, I reverted to a simpler route-driven structure for this iteration while keeping these abstractions in mind for future scalability or more complex applications.
Enhancing Error Handling

As part of the refactoring process, I implemented robust error handling for the random_number_api function. This ensures the application can gracefully handle issues such as API errors, network disruptions, or service unavailability. By introducing proper logging and fallback mechanisms, I improved the reliability and resilience of the application in handling external dependencies.
Challenges and Workflow Improvements

One of the primary challenges I faced during refactoring was dealing with breaking changes, particularly in models and routes, as I updated the codebase to reflect modern best practices. This required a strategic approach:

    Version Control and Branching: I utilized feature branches to experiment with changes while preserving the stability of the main application.
    Incremental Refactoring: Refactoring was performed in small, manageable increments, allowing for targeted testing and validation.
    Frontend Integration Testing: Each change in the backend was tested against the React frontend to ensure compatibility and functionality.

Through this process, I learned valuable lessons about planning and executing refactors, including the importance of incremental changes, thorough testing, and maintaining a stable workflow to minimize disruption. These practices not only helped resolve bugs more efficiently but also reinforced my understanding of how to approach large-scale refactoring projects systematically.


# import pytest
# from app import create_app, db
# from app.models.game import Game
# from app.models.guess import Guess
# # from app.models.person import User


# @pytest.fixture
# def app():
#     # create the app with a test config dictionary
#     app = create_app({"TESTING": True})

#     with app.app_context():
#         db.create_all()
#         yield app

#     # close and remove the temporary database
#     with app.app_context():
#         db.drop_all()


# @pytest.fixture
# def client(app):
#     return app.test_client()


# @pytest.fixture
# def one_guess(app):
#     with app.app_context():
#         game = Game(lives=10, difficulty_level=4,
#                     num_min=0, num_max=1, answer="1234")
#         guess = Guess(guess="1234")
#         game.guesses.append(guess)
#         db.session.add(game)
#         db.session.commit()
#         return guess


# @pytest.fixture
# def one_game(app):
#     with app.app_context():
#         game = Game(lives=10, difficulty_level=4,
#                     num_min=0, num_max=1, answer="1234")
#         db.session.add(game)
#         db.session.commit()
#         return game


# @pytest.fixture
# def one_user_with_game(app):
#     with app.app_context():
#         user = User(username="test_user", password="password")
#         game = Game(lives=10, difficulty_level=4,
#                     num_min=0, num_max=1, answer="1234")
#         user.games.append(game)
#         db.session.add(user)
#         db.session.commit()
#         return user


# if __name__ == "__main__":
#     pytest.main()

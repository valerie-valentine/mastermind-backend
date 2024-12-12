# from app import db


# class Guess(db.Model):
#     guess_id = db.Column(db.Integer, primary_key=True)
#     guess = db.Column(db.String, nullable=False)
#     correct_num = db.Column(db.Integer)
#     correct_loc = db.Column(db.Integer)
#     game_id = db.Column(db.Integer, db.ForeignKey(
#         "game.game_id"), nullable=False)
#     game = db.relationship("Game", back_populates="guesses")

#     def to_dict(self):
#         guess_dict = dict(
#             guess_id=self.guess_id,
#             guess=self.guess,
#             correct_num=self.correct_num,
#             correct_loc=self.correct_loc,
#             game_id=self.game_id,
#         )

#         print(guess_dict)

#         return guess_dict

#     @classmethod
#     def from_dict(cls, guess_data):
#         new_guess = cls(guess=guess_data["guess"])

#         return new_guess

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING
from app.helper_functions import *
from ..db import db

if TYPE_CHECKING:
    from .game import Game


class Guess(db.Model):
    # changed guess_id -> id
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guess: Mapped[str]
    correct_num: Mapped[int]
    correct_loc: Mapped[int]
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"), nullable=False)
    game: Mapped["Game"] = relationship(back_populates="guesses")

    def to_dict(self):
        guess_dict = dict(
            id=self.id,
            guess=self.guess,
            correct_num=self.correct_num,
            correct_loc=self.correct_loc,
            game_id=self.game_id,
        )

        print(guess_dict)

        return guess_dict

    @classmethod
    def from_dict(cls, game_data, guess_data):
        correct_num, correct_loc = check_client_guess(
            game_data, guess_data)

        new_guess = cls(
            guess=guess_data,
            correct_num=correct_num,
            correct_loc=correct_loc
        )

        return new_guess

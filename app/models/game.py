# from app import db


# class Game(db.Model):
#     game_id = db.Column(db.Integer, primary_key=True)
#     lives = db.Column(db.Integer, default=10)
#     difficulty_level = db.Column(db.Integer, default=4)
#     answer = db.Column(db.String)
#     num_min = db.Column(db.Integer, default=0)
#     num_max = db.Column(db.Integer, default=7)
#     game_status = db.Column(db.String, default="In Progress")
#     guesses = db.relationship(
#         "Guess", back_populates="game", cascade='all, delete-orphan', lazy=True)
#     timestamp = db.Column(db.DateTime, nullable=False,
#                           default=db.func.current_timestamp())
#     client_id = db.Column(db.Integer, db.ForeignKey(
#         "client.client_id"), nullable=True)
#     client = db.relationship("Client", back_populates="games")

#     def to_dict(self):
#         game_dict = dict(
#             game_id=self.game_id,
#             lives=self.lives,
#             difficulty_level=self.difficulty_level,
#             answer=self.answer,
#             num_min=self.num_min,
#             num_max=self.num_max,
#             game_status=self.game_status,
#             guesses=[guess.to_dict() for guess in self.guesses],
#             timestamp=self.timestamp)

#         if self.client_id:
#             game_dict["client_id"] = self.client_id

#         return game_dict

#     @classmethod
#     def from_dict(cls, game_data):
#         new_game = cls(
#             client_id=game_data.get("client_id"),
#             lives=game_data["lives"],
#             difficulty_level=game_data["difficulty_level"],
#             num_min=game_data["num_min"],
#             num_max=game_data["num_max"]
#         )

#         return new_game

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from sqlalchemy import DateTime, func
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from ..db import db
from app.helper_functions import random_number

if TYPE_CHECKING:
    from .client import Client
    from .guess import Guess


class Game(db.Model):
    # change game_id -> id
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    lives: Mapped[int]
    difficulty_level: Mapped[int]
    answer: Mapped[str]
    num_min: Mapped[int]
    num_max: Mapped[int]
    guesses: Mapped[list["Guess"]] = relationship(back_populates="game")
    game_status: Mapped[str] = mapped_column(
        String, default="In Progress", nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime, default=func.current_timestamp(), nullable=False)
    client_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("client.id"))
    client: Mapped[Optional["Client"]] = relationship(back_populates="games")

    def to_dict(self):
        game_dict = dict(
            id=self.id,
            lives=self.lives,
            difficulty_level=self.difficulty_level,
            answer=self.answer,
            num_min=self.num_min,
            num_max=self.num_max,
            game_status=self.game_status,
            guesses=[guess.to_dict() for guess in self.guesses],
            timestamp=self.timestamp)

        if self.client_id:
            game_dict["client_id"] = self.client_id

        return game_dict

    @classmethod
    def from_dict(cls, game_data):
        # if client id is in request (player logged in)
        client_id = game_data.get("client_id")

        new_game = cls(
            client_id=client_id,
            lives=game_data["lives"],
            difficulty_level=game_data["difficulty_level"],
            num_min=game_data["num_min"],
            num_max=game_data["num_max"],
            answer=random_number(
                game_data["difficulty_level"], game_data["num_min"], game_data["num_max"])
        )

        return new_game

    def check_game_over(self, guess, client):
        if guess.guess == self.answer:
            self.game_status = "Win"
            if client:
                client.score += 1
        else:
            self.lives -= 1
            if self.lives == 0:
                self.game_status = "Loss"

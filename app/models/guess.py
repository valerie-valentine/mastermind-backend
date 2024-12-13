from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional, TYPE_CHECKING
from app.helper_functions import *
from ..db import db

if TYPE_CHECKING:
    from .game import Game


class Guess(db.Model):
    guess_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guess: Mapped[str]
    correct_num: Mapped[Optional[int]] = mapped_column(nullable=True)
    correct_loc: Mapped[Optional[int]] = mapped_column(nullable=True)
    game_id: Mapped[int] = mapped_column(
        ForeignKey("game.game_id"), nullable=False)
    game: Mapped["Game"] = relationship(back_populates="guesses")

    def to_dict(self):
        guess_dict = dict(
            guess_id=self.guess_id,
            guess=self.guess,
            correct_num=self.correct_num,
            correct_loc=self.correct_loc,
            game_id=self.game_id,
        )

        print(guess_dict)

        return guess_dict

    @classmethod
    def from_dict(cls, guess_data):
        new_guess = cls(guess=guess_data)

        return new_guess

    def check_client_guess(self, game_data):
        correct_number = 0
        correct_location = 0
        answer_count = {}

        for num in game_data.answer:
            answer_count[num] = answer_count.get(num, 0) + 1

        for i, num in enumerate(self.guess):
            if num == game_data.answer[i]:
                correct_location += 1
            if num in answer_count and answer_count[num] > 0:
                correct_number += 1
                answer_count[num] -= 1

        self.correct_num = correct_number
        self.correct_loc = correct_location

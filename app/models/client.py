
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer
from ..db import db, bcrypt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import Game


class Client(db.Model):
    client_id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True)
    email: Mapped[str]
    password: Mapped[str]
    username: Mapped[str]
    score: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    games: Mapped[list["Game"]] = relationship(
        back_populates="client", cascade="all, delete-orphan")

    def to_dict(self):
        client_dict = dict(
            client_id=self.client_id,
            username=self.username,
            games=[game.to_dict() for game in self.games],
            score=self.score
        )

        return client_dict

    def to_dict_winners(self):
        client_dict = dict(
            username=self.username,
            score=self.score
        )

        return client_dict

    @classmethod
    def from_dict(cls, client_data):
        hashed_password = bcrypt.generate_password_hash(
            client_data["password"]).decode('utf-8')

        new_client = cls(
            username=client_data["username"],
            email=client_data["email"],
            password=hashed_password,
        )

        return new_client

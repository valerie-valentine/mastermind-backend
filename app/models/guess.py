from app import db


class Guess(db.Model):
    guess_id = db.Column(db.Integer, primary_key=True)
    guess = db.Column(db.String, nullable=False)
    correct_num = db.Column(db.Integer, nullable=False)
    correct_loc = db.Column(db.Integer, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey(
        "game.game_id"), nullable=False)
    game = db.relationship("Game", back_populates="guesses")


def to_dict(self):
    guess_dict = dict(
        guess_id=self.guess_id,
        guess=self.guess,
        correct_num=self.guess,
        correct_loc=self.correct_loc,
        game_id=self.game_id,
    )

    return guess_dict


def from_dict(cls, guess_data):
    new_guess = cls(
        guess=guess_data["guess"],
        game_id=guess_data["game_id"],
        correct_num=guess_data["correct_num"],
        correct_loc=guess_data["correct_loc"]
    )

    return new_guess

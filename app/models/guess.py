from app import db


class Guess(db.Model):
    guess_id = db.Column(db.Integer, primary_key=True)
    guess = db.Column(db.String, nullable=False)
    correct_num = db.Column(db.Integer, nullable=False)
    correct_loc = db.Column(db.Integer, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id"), nullable=True)
    game = db.relationship("Game", back_populates="guesses")

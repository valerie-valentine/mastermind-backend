from app import db


class Game(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    lives = db.Column(db.Integer, default=10, nullable=False)
    difficulty_level = db.Column(db.Integer, nullable=False, default=4)
    answer = db.Column(db.String, nullable=False)
    num_min = db.Column(db.Integer, default=0, nullable=False)
    num_max = db.Column(db.Integer, default=7, nullable=False)
    game_status = db.Column(db.String, nullable=False, default="In Progress")
    guesses = db.relationship("Guess", back_populates="game", lazy=True)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.user_id"), nullable=True)
    user = db.relationship("User", back_populates="games")

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

    def to_dict(self):
        game_dict = dict(
            game_id=self.game_id,
            lives=self.answer,
            difficulty_level=self.difficulty_level,
            answer=self.answer,
            num_min=self.num_min,
            num_max=self.num_max,
            game_status=self.game_status,
            guesses=self.guesses,
            time_stamp=self.timestamp)

        if self.user_id:
            game_dict["user_id"] = self.user_id

        return game_dict

    @classmethod
    def from_dict(cls, game_data):
        new_game = cls(
            user_id=game_data.get("user_id"),
            lives=game_data["lives"],
            difficulty_level=game_data["difficulty_level"],
            num_min=game_data["num_min"],
            num_max=game_data["num_max"],
            game_status=game_data["game_status"]
        )

        return new_game

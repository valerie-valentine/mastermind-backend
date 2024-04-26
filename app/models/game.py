from app import db


class Game(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    lives = db.Column(db.Integer, default=10)
    difficulty_level = db.Column(db.Integer, default=4)
    answer = db.Column(db.String)
    num_min = db.Column(db.Integer, default=0)
    num_max = db.Column(db.Integer, default=7)
    game_status = db.Column(db.String, default="In Progress")
    guesses = db.relationship(
        "Guess", back_populates="game", cascade='all, delete-orphan', lazy=True)
    timestamp = db.Column(db.DateTime, nullable=False,
                          default=db.func.current_timestamp())
    client_id = db.Column(db.Integer, db.ForeignKey(
        "client.client_id"), nullable=True)
    client = db.relationship("Client", back_populates="games")

    def to_dict(self):
        game_dict = dict(
            game_id=self.game_id,
            lives=self.lives,
            difficulty_level=self.difficulty_level,
            num_min=self.num_min,
            num_max=self.num_max,
            answer=self.answer,
            game_status=self.game_status,
            guesses=[guess.to_dict() for guess in self.guesses],
            timestamp=self.timestamp)

        if self.client_id:
            game_dict["client_id"] = self.client_id

        return game_dict

    @classmethod
    def from_dict(cls, game_data):
        new_game = cls(
            client_id=game_data.get("client_id"),
            lives=game_data["lives"],
            difficulty_level=game_data["difficulty_level"],
            num_min=game_data["num_min"],
            num_max=game_data["num_max"]
        )

        return new_game

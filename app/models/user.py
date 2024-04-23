from app import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    games = db.relationship("Game", back_populates="user", lazy=True)

    def to_dict(self):
        user_dict = dict(
            user_id=self.user_id,
            username=self.username,
            games=[game.to_dict() for game in self.games]
        )

        return user_dict

    @classmethod
    def from_dict(cls, user_data):
        new_user = cls(
            username=user_data["username"],
            password=user_data["password"],
        )

        return new_user

from app import db


class Client(db.Model):
    client_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    username = db.Column(db.String)
    score = db.Column(db.Integer, default=0)
    games = db.relationship("Game", back_populates="client",
                            cascade='all, delete-orphan', lazy=True)

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
        new_client = cls(
            username=client_data["username"],
            email=client_data["email"],
            password=client_data["password"],
        )

        return new_client

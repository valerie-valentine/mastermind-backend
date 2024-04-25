from app import db


class Client(db.Model):
    client_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, default=0, nullable=False)
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

    @classmethod
    def from_dict(cls, client_data):
        new_client = cls(
            username=client_data["username"],
            email=client_data["email"],
            password=client_data["password"],
        )

        return new_client

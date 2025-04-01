from db import db

class UserInteraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(500), nullable=False)
    bot_message = db.Column(db.String(500), nullable=False)

class SlangWord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False, unique=True)
    definition = db.Column(db.String(500), nullable=False)
    example = db.Column(db.String(500), nullable=True)
    popularity = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"<SlangWord {self.word}>"

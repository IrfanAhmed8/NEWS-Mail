from config import db

class BBC(db.Model):
    title = db.Column(db.String(100),primary_key=True)
    link=db.Column(db.String(300),nullable=True)
    content = db.Column(db.Text)
    image=db.Column(db.String(100))
    summary = db.Column(db.Text)


class Business(db.Model):
    title = db.Column(db.String(100),primary_key=True)
    link=db.Column(db.String(300),nullable=True)
    content = db.Column(db.Text)
    image=db.Column(db.String(100))
    summary = db.Column(db.Text)

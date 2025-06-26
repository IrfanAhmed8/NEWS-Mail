from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class BBC(db.Model):
    title = db.Column(db.String(100),primary_key=True)
    link=db.Column(db.String(300))
    content = db.Column(db.Text)
    image=db.Column(db.String(100))
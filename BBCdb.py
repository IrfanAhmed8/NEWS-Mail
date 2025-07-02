from config import db
import bcrypt

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



class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(300),nullable=True)
    email=db.Column(db.String(300),unique=True)
    password=db.Column(db.String(500),nullable=True)
      
    def __init__(self,name,email,password):
        self.name=name
        self.email=email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    

class user_Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Add ID for uniqueness
    email = db.Column(db.String(300))  # Remove unique=True to allow multiple rows
    frequency = db.Column(db.String(300), nullable=True)
    category = db.Column(db.String(300), nullable=True)  # Fix typo and use singular 'category'

    def __init__(self, email, frequency, category):
        self.email = email
        self.frequency = frequency
        self.category = category
        self.categories=category
        
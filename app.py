from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from BBCdb import BBC,db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BBC.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)




@app.route("/")
def hello_world():
    return render_template("home.html")


@app.route('/sports')
def sports():
    return render_template("sports.html")

@app.route('/politics')
def politics():
    return render_template("politics.html") 

@app.route('/business')
def business():
    return render_template("business.html")     

@app.route('/technology')
def technology():
    return render_template("technology.html")   

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("✅ Tables created:", db.inspect(db.engine).get_table_names())

    app.run(debug=True)
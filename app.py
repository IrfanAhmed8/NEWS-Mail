from flask import Flask,render_template


app = Flask(__name__)

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

app.run(debug=True)




from flask import Flask,render_template


app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("home.html")


@app.route('/sports')
def sports():
    return render_template("sports.html")

app.run(debug=True)




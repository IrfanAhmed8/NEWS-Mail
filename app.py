from flask import Flask,render_template
from apscheduler.schedulers.background import BackgroundScheduler
from flask_sqlalchemy import SQLAlchemy
from BBCdb import BBC,db,Business
from news_Scrapper import AlJazeeraScraper
def create_App():
    app = Flask(__name__)
    scrapper=AlJazeeraScraper("https://www.aljazeera.com")
    scheduler=BackgroundScheduler()
    scheduler.add_job(scrapper.scrape,trigger='interval',hours=1)
    scheduler.start()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BBC.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    
    @app.route("/")
    def hello_world():
        all_BBC_news=BBC.query.all()
        print("data is ready to be fetch")
        return render_template("home.html",all_news=all_BBC_news)


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

    return app 

if __name__ == "__main__":
    app=create_App()
    with app.app_context():
       
        db.create_all()
        print("✅ Tables created:", db.inspect(db.engine).get_table_names())

    app.run(debug=True)
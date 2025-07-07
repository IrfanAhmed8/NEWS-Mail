from flask import Flask,render_template,request,redirect,session,flash
from apscheduler.schedulers.background import BackgroundScheduler
from flask_sqlalchemy import SQLAlchemy
from BBCdb import BBC,db,businessDB,User,user_Subscription 
from news_Scrapper import AlJazeeraScraper
from businessTimes import businessScrapper
#from businessTimes import businessScrapper




def create_App():
    app = Flask(__name__)
    scrapper=AlJazeeraScraper("https://www.aljazeera.com")
    businessscrapper=businessScrapper("https://www.businesstoday.in/")
    scheduler=BackgroundScheduler()
    scheduler.add_job(scrapper.scrape,trigger='interval',hours=1)
    scheduler.add_job(businessscrapper.scrape,trigger='interval',hours=1)


    scheduler.start()
   
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///BBC.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key='NEWS-Mail'
    db.init_app(app)


    @app.route("/")
    def hello_world():
        all_BBC_news=BBC.query.all()
        print("data is ready to be fetch")
        if 'email' in session:
            user=User.query.filter_by(email=session['email']).first()
            return render_template("home.html",all_news=all_BBC_news,user=user)
        
        return redirect('/login')
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']

            # Make sure your User model has these fields
            try:
                user = User(name=name, email=email, password=password)
                db.session.add(user)
                db.session.commit()
            except:
                print("email already exist")

            return redirect('/login')  # Should redirect now if POST works
        return render_template('register.html')


    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form['email']
            password = request.form['password']
            
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session['email'] = user.email
                session['name']=user.name
                return redirect('/')
            else:
                return render_template('login.html', error="Invalid credentials")
        
        return render_template('login.html')
        
                
                


        



    
   
    

    @app.route('/logout')
    def logout():
        session.pop('email',None)
        return redirect('/login')
    
    @app.context_processor
    def inject_user():
        return dict(session_name=session.get('name'))


    @app.route('/sports')
    def sports():
        return render_template("sports.html")

    @app.route('/politics')
    def politics():
        return render_template("politics.html") 

    @app.route('/business')
    def business():
        all_business_news=businessDB.query.all()
        return render_template("business.html",business_news=all_business_news)     

    @app.route('/technology')
    def technology():
        return render_template("technology.html")  
    
    @app.route('/subscribe', methods=["GET", "POST"])
    def subscribe():
        if request.method == "POST":
            frequency = request.form.get('frequency')
            categories = request.form.getlist('category')  # checkbox inputs should use name="category"
            email = session.get('email')

            if email:
                # Optional: remove old entries
                user_Subscription.query.filter_by(email=email).delete()
                db.session.commit()

                for category in categories:
                    sub = user_Subscription(email=email, frequency=frequency, category=category)
                    db.session.add(sub)
                db.session.commit()

                flash("You are subscribed!", "success")
                return redirect('/')

            flash("You must be logged in to subscribe.", "danger")
            return redirect('/login')

        return render_template('subscribe.html')


    return app 

if __name__ == "__main__":
    app=create_App()
    with app.app_context():
        db.create_all()
        print("✅ Tables created:", db.inspect(db.engine).get_table_names())
    print ("app is runnig")
    app.run(debug=True)




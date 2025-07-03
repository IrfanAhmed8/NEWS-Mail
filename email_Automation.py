import smtplib
from BBCdb import user_Subscription
from app import create_App
# creates SMTP session


def email_Automation(sender_email,user_email):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    # start TLS for security
    s.starttls()
    # Authentication
    sender=sender_email
    s.login(sender, "jqfi nxyf lkrv moxh")
    # message to be sent
    message = "checking"
    # sending the mail
    
   
    s.sendmail(sender_email, user_email, message)
    # terminating the session
    s.quit()
if __name__ == "__main__":
    app=create_App()
    with app.app_context():
        emails=user_Subscription.query.all()
        for user in emails:
            if hasattr(user,'email'):
                email_Automation('jafriirfan37@gmail.com',user.email)
                print(f"email send to{user.email}")
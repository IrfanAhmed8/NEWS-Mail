import smtplib
from BBCdb import user_Subscription
from app import create_App
from email import encoders
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# creates SMTP session


def email_Automation(sender_email,user_email):
    password="jqfi nxyf lkrv moxh"
    filename = "Sports.pdf"
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        s.starttls()
        # Authentication
        sender=sender_email
        s.login(sender, password)
        # message to be sent
        message = "checking"
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = user_email
        message["Subject"] = "subject"
        message["Bcc"] = user_email  # Recommended for mass emails

        # Add body to email
        with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email    
            encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )
        

     # In same directory as script
    # sending the mail
    
    # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()
        s.sendmail(sender_email, user_email, text)
    except:
        print("there is some issue")

    finally:    
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
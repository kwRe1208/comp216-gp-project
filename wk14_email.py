import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailSender:
    def __init__(self):
        self.smtp_server = 'smtp.office365.com'
        self.smtp_port = 587
        self.sender_email = 'comp216-w24-gp1@hotmail.com'
        self.sender_password = 'Comp216@W24'
        self.email_subject = 'High temperature alert'
        self.recepient_email = 'ywong140@my.centennialcollege.ca'

    def send_email(self, message):
        try:
            print("Sending email...")
            # Create a multipart message and set headers
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = self.recepient_email
            msg['Subject'] = self.email_subject

            # Add body to the email
            msg.attach(MIMEText(message, 'plain'))

            # Create SMTP session for sending the email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
                print("Email sent successfully!")
        except Exception as e:
            print("An error occurred while sending the email:", str(e))

def main() -> None:
    email_sender = EmailSender()
    message = "The temperature is too high! Please check the system."
    email_sender.send_email(message)

if __name__ == "__main__":
    main()
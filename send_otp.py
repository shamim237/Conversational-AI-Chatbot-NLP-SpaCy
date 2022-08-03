from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import random

def send_otp(email):

    otp = random.randint(100000, 999999)
    msg = MIMEMultipart()
    message = "Your OTP is: " + str(otp)
    password = "shamim237x1602237"
    msg['From'] = "jiboneee237@gmail.com"
    msg['To'] = email
    msg['Subject'] = "OTP for Jarvis App"

    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    server.login(msg['From'], password)
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

    return otp
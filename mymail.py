import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def sendMail(body,toaddr):

    fromaddr = "sender@gmail.com"
    
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Series Info"


    msg.attach(MIMEText(body, 'plain','utf-8'))


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("sender@gmail.com", "mypassword")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)

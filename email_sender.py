from email.message import EmailMessage
import ssl
import smtplib


def send_email(subject, body):
    email_sender = 'lc906258462@gmail.com'
    email_password = 'lwqeomddqutripxo'
    email_receivers = ['cheng.li2@mail.mcgill.ca', 'saratvk1377@gmail.com', 'rui.song1029@gmail.com', 'sophearah.suy-puth@mail.mcgill.ca', 'sagar.nandeshwar@mail.mcgill.ca']

    subject = subject
    body = body

    for email_receiver in email_receivers:
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())
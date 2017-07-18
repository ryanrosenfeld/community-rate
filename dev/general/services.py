import binascii
import os


def send_email(user, pwd, recipient, subject, body):
    print("sending email")
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
    except Exception as e:
        print("Failed to send mail " + str(e))


def generate_reset_key(user):
    user.reset_key = binascii.hexlify(os.urandom(24))
    user.save()

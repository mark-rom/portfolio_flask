import os
import smtplib
from datetime import datetime
from email.message import EmailMessage

from dotenv import load_dotenv
from flask import Blueprint, redirect, render_template, request

load_dotenv()

MY_EMAIL = os.getenv('MY_EMAIL')
MY_PASS = os.getenv('MY_PASS')


bp = Blueprint('portfolio', __name__)


@bp.route('/')
def index():
    age = datetime.now().year - 1995
    return render_template('index.html', my_age=age)


@bp.route('/sendemail/', methods=['POST'])
def sendmail():
    if request.method == 'POST':
        name = request.form['name']
        subject = request.form['Subject']
        email = request.form['_replyto']
        message = request.form['message']
        my_email = MY_EMAIL
        my_password = MY_PASS

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(my_email, my_password)

    msg = EmailMessage()
    msg.set_content(
        'First name: ' + str(name)+'\nEmail:' + str(email) +
        '\nSubject:' + str(subject) + '\nMessage:' + str(message)
    )
    msg['To'] = my_email
    msg['From'] = email
    msg['Subject'] = subject

    try:
        server.send_message(msg)
        print('Send')

    except smtplib.SMTPResponseException:
        print('failed to send')

    return redirect('/')

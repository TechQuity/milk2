from flaskext.mail import Message

def send_awaiting_confirm_mail(user):
  
    subject = "We're waiting for your confirmation!!"
    mail_to_be_sent = Message(subject=subject, recipients=[user['Members_Email']])
    confirmation_url = url_for('activate_user', user_id=user['_id'],
_external=True)
    mail_to_be_sent.body = "Dear %s, click here to confirm: %s" %
(user['Members_Email'], confirmation_url)
    
    from routes import mail
    mail.send(mail_to_be_sent)
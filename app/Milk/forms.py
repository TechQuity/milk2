from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, SubmitField, validators, ValidationError, PasswordField
from wtforms.validators import Required
from models import db, User, UserReset
 
class ContactForm(Form):
  name = TextField("Name",  [validators.Required("Please enter your name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
  message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
  submit = SubmitField("Send")
  
  
class SignupForm(Form):
   Members_Email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
   Members_Password = PasswordField('New Password', [validators.Required("Please enter a password."),validators.EqualTo('confirm', message='Passwords must match')])
   confirm = PasswordField('Repeat Password')
   Members_First_Name = TextField("First name",  [validators.Required("Please enter your first name.")])
   Members_Last_Name = TextField("Last name",  [validators.Required("Please enter your last name.")])
   submit = SubmitField("Send")
   
   def __init__(self, *args, **kwargs):
      Form.__init__(self, *args, **kwargs)
 
   def validate(self):
      if not Form.validate(self):
        return False
      
      useremail = User.query.filter_by(Members_Email = self.Members_Email.data.lower()).first()
      if useremail:
         self.Members_Email.errors.append("That email is already taken")
         return False
      else:
         return True
      
  
class ChangePasswordForm(Form):
   Members_Password = PasswordField('New Password', [validators.Required("Please enter a password."),validators.EqualTo('confirm', message='Passwords must match')])
   confirm = PasswordField('Repeat Password')
   submit = SubmitField("Send")
   
   def __init__(self, *args, **kwargs):
      Form.__init__(self, *args, **kwargs)
 
   def validate(self):
      if not Form.validate(self):
        return False
      else:
        return True
      

class ForgottenPasswordForm(Form):
   Members_Email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
   submit = SubmitField("Send")
   
   def __init__(self, *args, **kwargs):
      Form.__init__(self, *args, **kwargs)
 
   def validate(self):
      if not Form.validate(self):
        return False

        
      useremail = User.query.filter_by(Members_Email = self.Members_Email.data.lower()).first()
      if useremail:
         return True
      else:
      	 self.Members_Email.errors.append("That email is not registered")
         return False     


class PasswordResetForm(Form):
   Members_Email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
   Temp_Password = PasswordField('Temporary Password', [validators.Required("Please enter your Temporary Password sent to you via email.")])
   Members_Password = PasswordField('New Password', [validators.Required("Please enter a password."),validators.EqualTo('confirm', message='Passwords must match')])
   confirm = PasswordField('Repeat Password')
   submit = SubmitField("Send")
   
   def __init__(self, *args, **kwargs):
      Form.__init__(self, *args, **kwargs)
 
   def validate(self):
      if not Form.validate(self):
        return False

        
      UserTempPassword = UserReset.query.filter_by(Members_Email = self.Members_Email.data.lower()).first()
      if UserTempPassword and UserTempPassword.check_password(self.Temp_Password.data):
         return True
      else:
         self.Members_Email.errors.append("That email has not requested a new password, or the Temporary Password is wrong")
         return False             
            
   
class SigninForm(Form):
  Members_Email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  Members_Password = PasswordField('Password', [validators.Required("Please enter a password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(Members_Email = self.Members_Email.data.lower()).first()
    if user and user.check_password(self.Members_Password.data):
      return True
    else:
      self.Members_Email.errors.append("Invalid e-mail or password")
      return False       	
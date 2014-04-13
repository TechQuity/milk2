from Milk import app
from flask import Flask, render_template, request, flash, session, url_for, redirect
from forms import ContactForm, SignupForm, SigninForm, ChangePasswordForm, ForgottenPasswordForm, PasswordResetForm
from flask.ext.mail import Message, Mail
from models import db, User ,update_password, UserReset, NoteSave
from werkzeug import generate_password_hash
from randomstring import id_generator
from datetime import datetime

mail = Mail()

@app.route('/testdb')
def testdb():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'
  
@app.route('/')
def home():
  return render_template('home.html')
  
@app.route('/about')
def about():
  return render_template('about.html')
  
@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='contact@example.com', recipients=[form.email.data])
      msg.body = """
      From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)

      return render_template('contact.html', success=True)

  elif request.method == 'GET':
    return render_template('contact.html', form=form)
  
  
@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
  
  if 'Members_Email' in session:
     return redirect(url_for('profile'))
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:   
      newuser = User(form.Members_Email.data, form.Members_Password.data, form.Members_First_Name.data, form.Members_Last_Name.data)
      db.session.add(newuser)
      db.session.commit()
      
      session['Members_Email']=newuser.Members_Email
      
      return redirect(url_for('profile'))
           
  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@app.route('/profile')
def profile():
 
  if 'Members_Email' not in session:
    return redirect(url_for('signin'))
 
  user = User.query.filter_by(Members_Email = session['Members_Email']).first()
  
 
  if user is None:
    return redirect(url_for('signin'))
  else:
    return render_template('profile.html')  
if __name__ == '__main__':
  app.run(debug=True)
  
  

  
@app.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
  form = ChangePasswordForm()

  if 'Members_Email' not in session:
    return redirect(url_for('signin'))
 
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('changepassword.html', form=form)
    else:   
      test = User.query.filter_by(Members_Email = session['Members_Email']).first()
      test.Members_Passhash = update_password(form.Members_Password.data)
      db.session.add(test)
      db.session.commit()
      return redirect(url_for('profile'))
                 
  elif request.method == 'GET':
    return render_template('changepassword.html', form=form)  

@app.route('/forgottenpassword', methods=['GET', 'POST'])
def forgottenpassword():
  form = ForgottenPasswordForm()
  temp_password = id_generator()

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('forgottenpassword.html', form=form)
    else:
      email = form.Members_Email.data
      
      user = User.query.filter_by(Members_Email = email).first()
      test = UserReset.query.filter_by(Members_Email = email).first()
      if test:
        db.session.delete(test)
        db.session.commit()

      msg = Message('Password Reset', sender='contact@example.com', recipients=[form.Members_Email.data])
      msg.body = """
      Hi %s, 
      You have clicked on the password reset link. Please find your temporary password below:
      %s
      Please go to the below link to reset your password:
      
      """ % (user.Members_First_Name, temp_password)
      mail.send(msg)

      member_reset = UserReset(form.Members_Email.data, temp_password, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
      db.session.add(member_reset)
      db.session.commit()
      return render_template('home.html', success=True)

  elif request.method == 'GET':
    return render_template('forgottenpassword.html', form=form)    

@app.route('/passwordreset', methods=['GET', 'POST'])
def passwordreset():
  form = PasswordResetForm()

   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('passwordreset.html', form=form)
    else:   
      test = User.query.filter_by(Members_Email = form.Members_Email.data).first()
      test.Members_Passhash = update_password(form.Members_Password.data)
      usertempdelete = UserReset.query.filter_by(Members_Email = form.Members_Email.data).first()
      db.session.add(test)
      db.session.delete(usertempdelete)
      db.session.commit()
      return redirect(url_for('profile'))
                 
  elif request.method == 'GET':
    return render_template('passwordreset.html', form=form)  

@app.route('/datasave', methods=['GET', 'POST'])
def datasave():
      note = NoteSave(Notes_Title,Notes_Note,Notes_Created_By,Notes_Created_On,Notes_Modified_By,Notes_Modified_On)
      db.session.add(note)
      db.session.commit()
     


  
  
@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
  
  if 'Members_Email' in session:
     return redirect(url_for('profile'))
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['Members_Email'] = form.Members_Email.data
      return redirect(url_for('profile'))
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form)  
    
    
@app.route('/signout')
def signout():
 
  if 'Members_Email' not in session:
    return redirect(url_for('signin'))
     
  session.pop('Members_Email', None)
  return redirect(url_for('home'))
  

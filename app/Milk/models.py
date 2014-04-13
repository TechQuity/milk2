from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
   __tablename__ = 'Members'
   Members_ID = db.Column(db.Integer, primary_key = True)
   Members_Email = db.Column(db.String(75), unique = True)
   Members_Passhash = db.Column(db.String(54))
   Members_First_Name = db.Column(db.String(45))
   Members_Last_Name = db.Column(db.String(45))

   def __init__ (self, Members_Email, Members_Password, Members_First_Name, Members_Last_Name):
    self.Members_Email = Members_Email.lower()
    self.set_Members_Password(Members_Password)
    self.Members_First_Name=Members_First_Name.title()
    self.Members_Last_Name=Members_Last_Name.title()
    
   def set_Members_Password(self, Members_Password):
     self.Members_Passhash = generate_password_hash(Members_Password)
     
   def check_password (self, Members_Password):
    return check_password_hash(self.Members_Passhash, Members_Password)
   
def update_password(password):
       return generate_password_hash(password)

class UserReset(db.Model):
    __tablename__ = 'Members_Reset'
    Members_Email = db.Column(db.String(30), primary_key = True)
    Members_TempPasshash = db.Column(db.String(128))
    Members_TempPassTime = db.Column(db.DateTime)

    def __init__ (self, Members_Email, Members_TempPassword, Members_TempPassTime):
      self.Members_Email = Members_Email.lower()
      self.set_Members_reset_password(Members_TempPassword)
      self.Members_TempPassTime =Members_TempPassTime

    def set_Members_reset_password(self,Members_TempPassword):
      self.Members_TempPasshash = generate_password_hash(Members_TempPassword)

    def check_password(self, Members_TempPassword):
      return check_password_hash(self.Members_TempPasshash,Members_TempPassword)

class NoteSave(db.Model):
    __tablename__ = 'Notes'
    Notes_ID = db.Column(db.Integer, primary_key = True)
    Notes_Title = db.Column(db.String(100))
    Notes_Note = db.Column(db.LargeBinary)
    Notes_Created_By = db.Column(db.String(30))
    Notes_Created_On = db.Column(db.DateTime)
    Notes_Modified_By = db.Column(db.String(30))
    Notes_Modified_On = db.Column(db.DateTime)

    def __init__(self,Notes_Title,Notes_Note,Notes_Created_By,Notes_Created_On,Notes_Modified_By,Notes_Modified_On):
      self.Notes_Title=Notes_Title
      self.Notes_Note=Notes_Note
      self.Notes_Created_By=Notes_Created_By
      self.Notes_Created_On=Notes_Created_On
      self.Notes_Modified_By=Notes_Modified_By
      self.Notes_Modified_On=Notes_Modified_On

      




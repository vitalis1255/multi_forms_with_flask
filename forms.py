# This is where forms for all html templates are created
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,RadioField,BooleanField
from wtforms.validators import DataRequired, Email, Length


#Step One Form
class PersonalInforForm(FlaskForm):
  """
  Handles Step One
  """
  #input type text
  name = StringField('Name',validators=[DataRequired(),Length(min=2,max=50)])
  email = StringField('Email',validators=[DataRequired(),Email()])
  phone = StringField('Phone',validators=[DataRequired(),Length(min=7,max=15)])
  submit = SubmitField('Next Step')


#Step Two Form
class PlanForm(FlaskForm):
  """
  Handles Step Two
  """
  plan = RadioField('Select Plan',choices=[
    ('arcade','Arcade'),
    ('advanced','Advanced'),
    ('pro','Pro'),
  ],default='arcade',validators=[DataRequired()])

  billing = RadioField('Billing Cycle',choices=[
    ('monthly','Monthly'),
    ('yearly','Yearly'),
  ],default='monthly',validators=[DataRequired()])

  submit = SubmitField('Next Step')



#Step three form
class AddonsForm(FlaskForm):
  """
  Handles Step Three
  """
  online_service = BooleanField('Online service')
  larger_storage = BooleanField('Larger storage')
  customizable_profile = BooleanField('Customizable profile')
  submit = SubmitField('Next Step')



#Step Four Form
class SummaryForm(FlaskForm):
  """
  Handles Summary Step Four
  """
  submit = SubmitField('confirm')

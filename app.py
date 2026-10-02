from flask import Flask, url_for, flash, render_template,redirect,session
from forms import PersonalInforForm, PlanForm, AddonsForm, SummaryForm
import json
import os
from datetime import datetime


app = Flask(__name__)

#create secret key
app.secret_key='app_form_mykey_is_on'


@app.route('/')
def index():
  """
  Index Home Page redirect to step 1
  """
  return redirect(url_for('step_one'))


@app.route('/multistep/step1', methods=['GET','POST'])
def step_one():
  #Get step one form
  form = PersonalInforForm()
  """
  Handles Step One function
  """
  #check if personal information exist
  if 'personal_info' in session and not form.is_submitted():
    form.name.data = session['personal_info'].get('name')
    form.email.data = session['personal_info'].get('email')
    form.phone.data = session['personal_info'].get('phone')

  #If personal info exists
  if form.validate_on_submit():
    session['personal_info'] = {
      'name': form.name.data,
      'email':form.email.data,
      'phone':form.phone.data,
    }
    return redirect(url_for('step_two'))# step_two is step two function.
  
  return render_template('multistep/step1.html',form=form, step=1)#step=1 indicate active.



@app.route('/multistep/step2',methods=['GET','POST'])
def step_two():
  """
  Handles step two
  """
  #Force a user to go back to step one if not filled
  if 'personal_info' not in session:
    return redirect(url_for('step_one'))# step_one is step one function.

  #get form two class
  form = PlanForm()

   #check if plan info exists
  if 'plan_info' in session and not form.is_submitted():
    form.plan.data = session['plan_info'].get('plan')
    form.billing.data = session['plan_info'].get('billing')

  #if plan info exists
  if form.validate_on_submit():
    session['plan_info'] = {
      'plan':form.plan.data,
      'billing':form.billing.data,
    }
    return redirect(url_for('step_three'))# step_three is step three function.

  return render_template('/multistep/step2.html',form=form,step=2)#step=2 makes it active.


@app.route('/multistep/step3', methods=['GET','POST'])
def step_three():
  """
  Handles step three
  """
  #force the user to go back to step if plan not exists
  if 'plan_info' not in session:
    return redirect(url_for('step_two'))# step_two is step two function.

  #Get step three form class
  form = AddonsForm()

  #check if addons info exists in session and form submission
  if 'addons_info' in session and not form.is_submitted():
    form.online_service.data = session['addons_info'].get('online_service')
    form.larger_storage.data = session['addons_info'].get('larger_storage')
    form.customizable_profile.data = session['addons_info'].get('customizable_profile')

  #if addons info exists
  if form.validate_on_submit():
    session['addons_info'] = {
      'online_service':form.online_service.data,
      'larger_storage':form.larger_storage.data,
      'customizable_profile':form.customizable_profile.data,
    }
    return redirect(url_for('step_four'))#step_four is step four function.

  return render_template('multistep/step3.html',form=form,step=3)# step=3 will make active


@app.route('/multistep/step4',methods=['GET','POST'])
def step_four():
  """
  Handles step four
  """

  #check addons info exist in step three
  if 'addons_info' not in session:
    return redirect(url_for('step_three'))

  #Get class four form
  form = SummaryForm()


  summary_data = {
    'personal':session.get('personal_info'),
    'plan':session.get('plan_info'),
    'addons':session.get('addons_info'),
    'submitted_at': datetime.now().strftime("%Y-%m-%d" "%H:%M:%S")
  }

  if form.validate_on_submit():
    #create folder if not exist
    folder_name = 'submissions'
    os.makedirs(folder_name, exist_ok=True)

    # Get username and create a filename with it 
    name = summary_data.get('personal', {}).get('name','user')
    safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_','-')).strip().replace(' ','_')

    # Add a short timestamp to prevent overwriting if same user submits twice

    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_name}_{timestamp_str}.json"

    file_path =os.path.join(folder_name,filename)

    # save the dictionary as JSON file inside the folder
    with open(file_path, 'w', encoding='utf-8') as f:
      json.dump(summary_data,f,indent=4)

    # clear session state after successful save
    session.clear()

    flash(
      f"Thank you, {name}! Your application has been saved successfully."
    )
    return redirect(url_for('step_one'))
  return render_template('multistep/step4.html',form=form,step=4)


if __name__ == '__main__':
  app.run(debug=True)
# to-do list flask app

import os
from flask import Flask,request,render_template
from datetime import date
from twilio.rest import Client
from flask_mail import Mail, Message
import datetime

app = Flask(__name__)


datetoday2 = datetime.datetime.now().strftime('%Y-%m-%d')  # Define the variable

# Twilio Credentials (შეიცვალეთ თქვენი მონაცემებით)
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
from_phone = os.getenv('TWILIO_PHONE_NUMBER')

# Flask-Mail კონფიგურაცია
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = print(os.getenv('MAIL_PORT')) 
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')   # თქვენი Gmail მისამართი
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD') # თქვენი Gmail პაროლი

mail = Mail(app)

# Twilio SMS გაგზავნის ფუნქცია
def send_sms(to_phone, body):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=body,
        from_=from_phone,
        to=to_phone
    )
    print(f"SMS sent successfully: {message.sid}")

# Flask-Mail ელ. ფოსტის გაგზავნის ფუნქცია
def send_email(email, task, deadline):
    subject = "მოახლოებული დედლაინი"
    body = f"მოგესალმებით!\n\n თქვენ მიერ შერჩეული პროექტზე:{task}\nრეგისტრაცია სრულდება {deadline}.\n\n გისურვებთ წარმატებებს!"
    
    msg = Message(subject, recipients=[email], body=body)
    try:
        mail.send(msg)
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

# Flask-ის როუტი დავალების დასამატებლად
@app.route('/addtask', methods=['POST'])
def add_task():
    task = request.form.get('newtask')
    user_email = request.form.get('email')  # ელ. ფოსტის მისამართი
    user_phone = request.form.get('phone')  # ტელეფონის ნომრის მიღება
    deadline = request.form.get('deadline')  # დედლაინი

    # დავალების შენახვა ფაილში
    with open('tasks.txt', 'a') as f:
        f.writelines(f"{task}\n")

    # SMS გაგზავნა
    if user_phone:
        send_sms(user_phone, f"მოგესალმებით! თქვენ მიერ შერჩეულ პროექტზე {task}\nრეგისტრაცია სრულდება {deadline}. გისურვებთ წარმატებებს!")
    print(task, deadline)
    # ელ. ფოსტის გაგზავნა
    if user_email:
        send_email(user_email, task, deadline)

    return render_template('home.html', datetoday2=datetoday2, tasklist=gettasklist(), l=len(gettasklist()))

# მთავარი გვერდი
@app.route('/')
def home():
    return render_template('home.html', datetoday2=datetoday2, tasklist=gettasklist(), l=len(gettasklist()))

# დავალების სიის ამოღება
def gettasklist():
    with open('tasks.txt', 'r') as f:
        tasklist = f.readlines()
    return tasklist

if __name__ == '__main__':
    app.run(debug=True, port=5001)



#### Saving Date today in 2 different formats
datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")


#### If this file doesn't exist, create it
if 'tasks.txt' not in os.listdir('.'):
    with open('tasks.txt','w') as f:
        f.write('')


def gettasklist():
    with open('tasks.txt','r') as f:
        tasklist = f.readlines()
    return tasklist

def createnewtasklist():
    os.remove('tasks.txt')
    with open('tasks.txt','w') as f:
        f.write('')

def updatetasklist(tasklist):
    os.remove('tasks.txt')
    with open('tasks.txt','w') as f:
        f.writelines(tasklist)


################## ROUTING FUNCTIONS #########################

#### Our main page
@app.route('/')
def home():
    return render_template('home.html',datetoday2=datetoday2,tasklist=gettasklist(),l=len(gettasklist())) 


# Function to clear the to-do list
@app.route('/clear')
def clear_list():
    createnewtasklist()
    return render_template('home.html',datetoday2=datetoday2,tasklist=gettasklist(),l=len(gettasklist())) 


# Function to add a task to the to-do list
@app.route('/addtask',methods=['POST'])
def add_task():
    task = request.form.get('newtask')
    with open('tasks.txt','a') as f:
        f.writelines(task+'\n')
    return render_template('home.html',datetoday2=datetoday2,tasklist=gettasklist(),l=len(gettasklist())) 


# Function to remove a task from the to-do list
@app.route('/deltask',methods=['GET'])
def remove_task():
    task_index = int(request.args.get('deltaskid'))
    tasklist = gettasklist()
    print(task_index)
    print(tasklist)
    if task_index < 0 or task_index > len(tasklist):
        return render_template('home.html',datetoday2=datetoday2,tasklist=tasklist,l=len(tasklist),mess='Invalid Index...') 
    else:
        removed_task = tasklist.pop(task_index)
    updatetasklist(tasklist)
    return render_template('home.html',datetoday2=datetoday2,tasklist=tasklist,l=len(tasklist)) 
    
@app.route('/clear', methods=['GET'])
def clear():
    # Your clear logic here
    return "Cleared successfully!"  # Or some other response

#### Our main function which runs the Flask App
if __name__ == '__main__':
    app.run(debug=True, port=5001)
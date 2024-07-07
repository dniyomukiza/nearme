import random,os
from datetime import datetime,timedelta
from flask import Blueprint,render_template,request,flash,redirect,url_for,session
from flask_login import login_user, current_user, login_required, logout_user,LoginManager,login_manager
from .extensions import db
from .models import User
from .forms import *
from re import search
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
main= Blueprint("main", __name__)

#Render the home page
@main.route("/",methods=['POST','GET'])
def home():
    if request.method == 'POST':

        hours = int(request.form['hours'])
        minutes = int(request.form['minutes'])
        
        # Calculate total minutes
        total_minutes = hours * 60 + minutes
        total_price = total_minutes * 0.95

        flash(f'The estimate total price is : ${total_price}')

    return render_template('home.html')

# Register the user
@main.route('/register', methods=['GET', 'POST'])
def register():
    logout_user()
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user_username = form.username.data
        new_user_password = form.password.data
        new_user_email=form.email.data
        new_user_phone=form.phone.data
        new_user_fname=form.fname.data
        new_user_lname=form.lname.data
        if len(new_user_username) < 7 or search("[\d]+", new_user_username) == None or search("[A-Z]+", new_user_username) == None :
            flash("You need at least 7 characters with one uppercase and a digit")
        elif len(new_user_password) < 8 or search("[A-Z]+", new_user_password) == None or search("[_@#$]+", new_user_password) == None:
            flash("Password must be at least 8 characters with capital letter and a symbol")
        else:
            db.session.add(User(username=new_user_username, password=new_user_password,email=new_user_email,phone=new_user_phone,first_name=new_user_fname,last_name=new_user_lname))
            db.session.commit()
            flash(f'Your account has been successfully created! Please login below')
            return redirect(url_for('main.home'))
    return render_template('register.html', title='Register', form=form)

@main.route("/login", methods=['GET', 'POST'])
def login():
    logout_user()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        # Query the user from the database based on username
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password', 'error')
            return redirect(url_for('main.login'))
        user_email = user.email
        session['user_email'] = str(user_email) 
        # Login the user using Flask-Login
        login_user(user, remember=form.remember_me.data)
        send_email(user_email)
        return redirect(url_for('main.otp'))

    return render_template("login.html", title='Login', form=form)

@main.route('/otp', methods=['GET', 'POST'])
def otp():
    form = OTPForm()

    if form.validate_on_submit():
        entered_otp = form.otp_code.data
        expected_otp = session.get('expected_otp')  # Retrieve the OTP from the session
        
        if entered_otp == expected_otp:
            flash('Account verified successfully!', 'success')
            return redirect(url_for('main.reserve'))
        flash('Incorrect OTP code. Please login again to generate a new code','error')
        logout_user()
        return redirect(url_for('main.login'))

    return render_template('otp.html', form=form)

def send_email(email,subject=None, body=None):
    try:
        otp = otp_generate()
        session['expected_otp'] = str(otp)  # Store the OTP in the session
        # Retrieve environment variables
        conf_email = os.environ.get("CONF_EMAIL")
        conf_code = os.environ.get("CONF_CODE")
        sender_email = os.environ.get("SENDER_EMAIL")
        if not conf_email or not conf_code or not sender_email:
            return "Environment variables not properly set."
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, conf_code)

        # Create the email content
        subject = 'OTP code'
        body = f'Verification code: {otp}'
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Send the email
        action = server.sendmail(sender_email, email, message.as_string())
        server.quit()
        return action
    except Exception as e:
        return f"Failed to send OTP: {e}"

def otp_generate():
    return random.randint(10000, 99999)

@main.route('/reserve', methods=['GET', 'POST'])
def reserve():
    form = ReservationForm()
    hours = range(1, 13)  # 12-hour format
    minutes = [f"{i:02d}" for i in range(0, 60)]
    am_pm_choices = ['AM', 'PM']
    available_times = [(f"{h:02d}:{m} {ap}", f"{h:02d}:{m} {ap}") for h in hours for m in minutes for ap in am_pm_choices]
    form.start_time.choices = available_times
    form.end_time.choices = available_times
    if form.validate_on_submit():
        location = form.location.data
        date = form.date.data
        start_time_str = form.start_time.data
        end_time_str = form.end_time.data
        message = form.message.data

        start_time = datetime.strptime(start_time_str, '%I:%M %p').time()
        end_time = datetime.strptime(end_time_str, '%I:%M %p').time()

        start_dt = datetime.combine(date, start_time)
        end_dt = datetime.combine(date, end_time)

        # Calculate total duration in minutes
        duration_minutes = (end_dt - start_dt).seconds // 60

        # Calculate total amount owed
        cost_per_minute = 0.95
        total_amount = duration_minutes * cost_per_minute
        doc=f"Reservations details\n\nDate: {date}\nStart Time: {start_time_str}\nEnd Time: {end_time_str}\nLocation: {location}\nTotal Time: {duration_minutes} minutes\nTotal Amount : ${total_amount:.2f}\nMessage: {message}"
        subject = "Customer's reservation"
        body = doc 
        send_details(subject,body)
        return redirect(url_for('main.home', total_time=duration_minutes, total_amount=total_amount))

    return render_template('reserve.html', form=form)

def send_details(subject=None, body=None,recipients=None):
    if recipients is None:
        user_email=session.get('user_email')
        recipients=[os.environ.get("SENDER_EMAIL"),user_email]
    print(', '.join(recipients))
    try:
        conf_email = os.environ.get("CONF_EMAIL")
        conf_code = os.environ.get("CONF_CODE")
        sender_email = os.environ.get("SENDER_EMAIL")
        if not conf_email or not conf_code or not sender_email:
            return "Environment variables not properly set."
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, conf_code)

        # Create the email content
        subject = 'Reservation details'
        body = body
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = ', '.join(recipients)
        email=os.environ.get("MY_EMAIL")
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Send the email
        action = server.sendmail(sender_email, recipients, message.as_string())
        server.quit()
        return action
    except Exception as e:
        return f"Failed to send details: {e}"
    
@main.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        def send_message():
            conf_email = os.environ.get("CONF_EMAIL")
            conf_code = os.environ.get("CONF_CODE")
            sender_email = os.environ.get("SENDER_EMAIL")
            if not conf_email or not conf_code or not sender_email:
                return "Environment variables not properly set."
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, conf_code)

            # Create the email content
            subject = 'Contact form'
            message=f'First name: {form.FirstName.data}\nLast name: {form.LastName.data} \nPhone: {form.phone.data} \nEmail: {form.email.data}\nMessage: {form.message.data}'
            body = message
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = os.environ.get("SENDER_EMAIL")
            email=os.environ.get("MY_EMAIL")
            message['Subject'] = subject
            message.attach(MIMEText(body, 'plain'))

            # Send the email
            action = server.sendmail(sender_email,email, message.as_string())
            server.quit()
            return action
        send_message()
        flash("We will get back to you shortly!")    
        return redirect(url_for('main.home'))
    return render_template("contact.html",form=form)

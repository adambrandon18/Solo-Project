from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.model import Member
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)  #importinf bcrypt and making a instance and passing in app

@app.route('/')
def index():
    return render_template('LoginAndRegistration.html')

@app.route('/login', methods =['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    member = Member.get_by_email(data)
    if not member:
        flash("Wrong Login Information!!!!!!!!", "Login" ) 
        return redirect('/')
    if not bcrypt.check_password_hash(member.password, request.form['password']):
        flash("Invalid login information, Sorry")
        return redirect('/')
    session['member_id'] = member.id
    return redirect('/member_dashboard')

@app.route('/logout')
def logout():
    session.clear()  #ends the user info and stops and prevents unwanted eyes on provate information
    return redirect('/')

@app.route('/member_dashboard')
def member_dashboard():
    if not 'member_id' in session: #they nave no buiness in the login if their are not insession/active user
        print("member not logged in")
        return redirect('/logout') #redirects to logout and clears the ession in the logout
    data ={
        'id': session['member_id'] #we are retrieving the info with the session id
    }
    print("Logging in")
    return render_template("member_dashboard.html",member=Member.get_by_id(data))

@app.route('/registration',methods=['POST'])
def registration():

    if not Member.validate_register(request.form):  #is_valid was not defined so i have to use validate_register
        return redirect('/')
    data ={                 #creation of our user object
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = Member.save(data)  #here we are saving the user object we just created on the line above
    session['member_id'] = id # put into session because on the dashboard page we wanna make sure they are in session

    return redirect('/member_dashboard') #once redirected to the dashboard session should be active and our user should be logged in
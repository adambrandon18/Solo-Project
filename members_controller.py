from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.vehicles_model import Vehicle #importing Car class
from flask_app.models.members_model import Member #importing User class
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)  #importinf bcrypt and making a instance and passing in app

@app.route('/start')
def start():
    return render_template('LoginAndRegistration.html')


#...............................................................................................
@app.route('/login', methods =['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    member = Member.get_by_email(data)
    if not member:
        flash("Incorrect Info Champ!!! try again", "Login" )
        return redirect('/')
    if not bcrypt.check_password_hash(member.password, request.form['password']):
        flash("Wrong Info Champ!!!")
        return redirect('/')
    session['member_id'] = member.id
    return redirect('/member_dashboard')


@app.route('/member_dashboard')
def member_dashboard():
    if not 'member_id' in session:
        return redirect('/logout')
    data ={
        'id': session['member_id']
    }
    print("Logging In")
    return render_template("member_dashboard.html", vehicles = Vehicle.get_all_w_members(), member = Member.get_by_id(data))

@app.route('/logout')
def logout():
    session.clear()  #ends the user info and stops and prevents unwanted eyes on provate information
    return redirect('/start')
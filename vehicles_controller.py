from flask_app import app #, send_from_directory
import os
from flask import render_template,redirect,session,request,flash, url_for
from flask_app.models import members_model, vehicles_model

from werkzeug.utils import secure_filename
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)  #importinf bcrypt and making a instance and passing in app
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


@app.route('/')
def index():
    return render_template('LoginAndRegistration.html')

@app.route('/registration',methods=['POST'])    #user controller
def registration():

    if not members_model.Member.validate_register(request.form):  #is_valid was not defined so i have to use validate_register
        return redirect('/')
    data ={                 #creation of our user object
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = members_model.Member.save(data)  #here we are saving the user object we just created on the line above
    session['member_id'] = id # put into session because on the dashboard page we wanna make sure they are in session

    return redirect('/member_dashboard') #once redirected to the dashboard session should be active and our user should be logged in


@app.route('/vehicle/new')  #route the create recipe button uses to get to create recipe page
def new():
    return render_template("new_vehicle.html")

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS  #checks the file to make sure it has appropiate exts


#@app.route('/uploads/<name>')
#def download_file(name):
#    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/vehicle/create',methods=['POST'])
def create():
    print(request.form)
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        print("hi")
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #return redirect('/member_dashboard')
    if not vehicles_model.Vehicle.validate_vehicle(request.form):
        return redirect('/vehicle/new')

    # Create a dictionary/copy of request.form.
    d_copy = request.form.copy() 

    # Add "filename": actual_file_name to that dictionary
    d_copy['image'] = f"/static/uploads/{filename}"
    print(request.form)
    print("*********",filename)
    vehicles_model.Vehicle.save(d_copy)
    # vehicles_model.Vehicle.save(d_copy)
    # vehicles_model.Vehicle.save(request.form, filename) OPTION 2
    # XXXXXXXXX Need to go through DB table and related queries,
    # update them to include filename in the table and in the queries.
    return redirect('/member_dashboard')

@app.route('/vehicle/edit/<int:id>')   #recipe id
def edit(id):
    data ={
        "id":id
    }
    return render_template("edit_vehicle.html", vehicle=vehicles_model.Vehicle.get_one_vehicle_w_member(data))

@app.route('/vehicle/update',methods=['POST'])
def update():
    print(request.form)
    vehicles_model.Vehicle.update(request.form)
    return redirect('/member_dashboard')

@app.route('/vehicle/show/<int:id>')
def show(id):
    data ={ 
        "id":id
    }
    return render_template("show_vehicle.html",vehicle=vehicles_model.Vehicle.get_one_vehicle_w_member(data))



@app.route('/vehicle/delete/<int:id>')
def delete(id):
    data ={
        'id': id
    }
    print("data controller", data)
    vehicles_model.Vehicle.delete(data)
    return redirect('/member_dashboard')
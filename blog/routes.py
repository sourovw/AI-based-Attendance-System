import os
from blog import app, db, bcrypt
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from blog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from blog.recognizer import face_recognizer
from blog.save_img import save_picture
from blog.models import User


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Invalid credentials.', 'danger')
    
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, full_name=form.full_name.data, email=form.email.data,
                    varsity=form.varsity.data, password=hashed_password)
        
        os.makedirs('blog/static/faces/' + form.username.data)
        src = './blog/static/extras/default.png'
        dst = './blog/static/faces/' + form.username.data + '/default.png'

        with open(src, 'rb') as f:
            data = f.read()
        with open(dst, 'wb') as f:
            f.write(data)
            print("File copied")
        
        db.session.add(user)
        db.session.commit()

        flash('Your account has been created. You are now able to log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.pic1.data:
            pic1 = save_picture(form.pic1.data)
            current_user.img1 = pic1
        
        if form.pic2.data:
            pic2 = save_picture(form.pic2.data)
            current_user.img2 = pic2
        
        if form.pic3.data:
            pic3 = save_picture(form.pic3.data)
            current_user.img3 = pic3
        
        current_user.username = form.username.data
        current_user.full_name = form.full_name.data
        current_user.email = form.email.data
        current_user.varsity = form.varsity.data
        db.session.commit()
        
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.full_name.data = current_user.full_name
        form.email.data = current_user.email
        form.varsity.data = current_user.varsity

    uname = current_user.username
    fname = 'faces/' + uname + '/'
    
    img1 = url_for('static', filename = fname + current_user.img1)
    img2 = url_for('static', filename = fname + current_user.img2)
    img3 = url_for('static', filename = fname + current_user.img3)
    imgs = [img1, img2, img3]

    return render_template('profile.html', title='Profile', imgs=imgs, form=form)
    

@app.route("/attendance", methods=['GET', 'POST'])
@login_required
def attendance():
    return render_template('attendance.html', title='Attendance')


@app.route("/classify-face", methods=['GET', 'POST'])
@login_required
def classify_face():
    face_recognizer()
    return render_template('processed.html', title='Classify Face')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

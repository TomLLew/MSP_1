from flask import render_template, redirect, url_for, request
from application import app, db, bcrypt
from application.models import User, Post
from application.forms import PostForm, LoginForm, RegistrationForm
from flask_login import login_user, current_user, logout_user, login_required
from random import randint
import boto3
import pymysql
from werkzeug import secure_filename

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Homepage')

@app.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    postData = Post.query.all()
    image = User.query.filter_by(id=current_user.id).all()
    payload = "https://msp-1-bucket-1579257693.s3.amazonaws.com/"+image['image']
    print(payload)
    return render_template('posts.html', title='Posts', posts=postData, picture=payload)

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('post'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')

            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('posts'))

    return render_template('login.html', title='Posts', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    random = randint(0, 999999)
    if current_user.is_authenticated:
        return redirect(url_for('posts'))
    form = RegistrationForm()
    if form.validate_on_submit():
        filename = secure_filename(form.profile_pic.data.filename)
        i_id = 'images/' + str(random) + filename
        s3 = boto3.resource('s3')
        s3.Bucket('msp-1-bucket-1579257693').put_object(Key=i_id, Body=request.files["profile_pic"] )
        hashed_pw = bcrypt.generate_password_hash(form.password.data)
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password=hashed_pw, image=i_id)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    user = User.query.get(current_user.id)
    logs = Workout.query.filter_by(user_id=current_user.id).all()
    print(logs)
    for log in logs:
        db.session.delete(log)
        db.session.commit()
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('register'))
    except:
        return redirect(url_for('account'))

@app.route('/create', methods=['GET','POST'])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        postData = Post(
            post=form.post.data,
            user_id=current_user.id
        )

        db.session.add(postData)
        db.session.commit()
        return redirect(url_for('posts'))
    else:
        print(form.errors)
    return render_template('create_post.html', title='Create Post', form=form)

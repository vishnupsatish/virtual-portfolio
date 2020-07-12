import os
import datetime
import secrets
import cloudinary
import cloudinary.uploader
import cloudinary.api
from flask import render_template, url_for, flash, redirect, request, abort
from portfolio import app, db, bcrypt
from portfolio.forms import (RegistrationForm, LoginForm, AddJobForm, AddAchievementForm, AddProjectForm, UpdateProfileForm)
from portfolio.models import User, Job, Achievement, Project
from flask_login import login_user, current_user, logout_user, login_required
import requests
import io

cloud_name = os.environ['CLOUDINARY_CLOUD_NAME']
api_key = os.environ['CLOUDINARY_API_KEY']
api_secret = os.environ['CLOUDINARY_API_SECRET']

cloudinary.config(
    cloud_name=cloud_name,
    api_key=api_key,
    api_secret=api_secret
)



@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    form = UpdateProfileForm()
    if request.method == "GET":
        form.bio.data = current_user.bio
        form.skills.data = current_user.skills
    if form.validate_on_submit():
        current_user.bio = form.bio.data
        current_user.skills = form.skills.data
        if form.resume.data:
            pdf_name = secrets.token_hex(16)
            current_user.resume = pdf_name
            cloudinary.uploader.upload(form.resume.data, public_id=pdf_name)
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('home'))

    return render_template('home.html', page_title="Home", form=form, current_user=current_user, cloud_name=cloud_name)


@app.route('/delete_resume', methods=['POST'])
def delete_resume():
    if not current_user.is_authenticated:
        return redirect(url_for('home'))
    if current_user.resume == "":
        return redirect(url_for('home'))
    cloudinary.uploader.destroy(current_user.resume)
    current_user.resume = ""
    db.session.commit()
    flash('Your resume has been deleted.', 'info')
    return redirect(url_for('home'))


@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    form = AddJobForm()
    if form.validate_on_submit():
        job = Job(company_name=form.name.data, description=form.description.data,
        employee=current_user, start_date=datetime.datetime.strptime(form.start_date.data, "%b %d, %Y"), end_date=datetime.datetime.strptime(form.end_date.data, "%b %d, %Y"), volunteer=form.volunteer.data, role=form.role.data) if form.end_date.data != "" else Job(company_name=form.name.data, description=form.description.data, employee=current_user, start_date=datetime.datetime.strptime(form.start_date.data, "%b %d, %Y"), volunteer=form.volunteer.data, role=form.role.data)
        db.session.add(job)
        db.session.commit()
        return redirect(url_for('jobs'))
    elif (not form.validate_on_submit()) and request.method == "POST":
        flash('There has been an error. Click on the + button to see the error.', 'error')
    return render_template('jobs.html', form=form, jobs=current_user.jobs)

@app.route('/achievements', methods=['GET', 'POST'])
def achievements():
    form = AddAchievementForm()
    if form.validate_on_submit():
        achievement = Achievement(name=form.name.data, description=form.description.data, year=form.year.data, winner=current_user)
        db.session.add(achievement)
        db.session.commit()
        return redirect(url_for('achievements'))
    elif (not form.validate_on_submit()) and request.method == "POST":
        flash('There has been an error. Click on the + button to see the error.', 'error')
    return render_template('achievements.html', page_title='Achievements', form=form, achievements=current_user.achievements)

@app.route('/projects', methods=['GET', 'POST'])
def projects():
    form = AddProjectForm()
    if form.validate_on_submit():
        project = Project(name=form.name.data, year=form.year.data, url=form.url.data, description=form.description.data, creator=current_user)
        db.session.add(project)
        db.session.commit()
        return redirect(url_for('projects'))
    elif (not form.validate_on_submit()) and request.method == "POST":
        flash('There has been an error. Click on the + button to see the error.', 'error')
    return render_template('projects.html', page_title='Projects', form=form, projects=current_user.projects)


@app.route("/about")
def about():
    return render_template('about.html', page_title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, name=form.name.data, token=secrets.token_hex(16), bio=form.bio.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', page_title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'error')
    return render_template('login.html', page_title='Login', form=form)


@app.route('/static_site')
def static_site():
    return render_template('static_site.html', page_title=current_user.name, current_user=current_user)

@app.route('/static_site/jobs')
def staticjobs():
    return render_template('staticjobs.html', page_title=current_user.name, jobs=current_user.jobs)

@app.route('/static_site/achievements')
def staticachievements():
    return render_template('staticachievements.html', page_title=current_user.name, achievements=current_user.achievements)

@app.route('/static_site/projects')
def staticprojects():
    return render_template('staticprojects.html', page_title=current_user.name, projects=current_user.projects)

@app.route('/edit/project/<int:id>', methods=["GET", 'POST'])
def edit_projects(id):
    project = Project.query.filter_by(id=id).first_or_404()
    if project.creator != current_user:
        abort(403)
    form = AddProjectForm()
    if form.validate_on_submit():
        project.name = form.name.data
        project.description = form.description.data
        project.year = form.year.data
        project.url = form.url.data
        db.session.commit()
        flash('Your changes have been made.', 'success')
        return redirect(url_for('home'))
    form.name.data = project.name
    form.description.data = project.description
    form.year.data = project.year
    form.url.data = project.url
    return render_template('edit_projects.html', form=form)
    
@app.route('/edit/job/<int:id>', methods=["GET", 'POST'])
def edit_jobs(id):
    job = Job.query.filter_by(id=id).first_or_404()
    if job.employee != current_user:
        abort(403)
    form = AddJobForm()
    if form.validate_on_submit():
        job.company_name = form.name.data
        job.role = form.role.data
        job.description = form.description.data
        job.start_date = datetime.datetime.strptime(form.start_date.data, "%b %d, %Y")
        if form.end_date.data != "":
            job.end_date = datetime.datetime.strptime(form.end_date.data, "%b %d, %Y")
        job.volunteer = form.volunteer.data
        db.session.commit()
        flash('Your changes have been made.', 'success')
        return redirect(url_for('home'))
    form.name.data = job.company_name
    form.role.data = job.role
    form.description.data = job.description
    form.start_date.data = job.start_date.strftime("%b %d, %Y")
    form.end_date.data = job.end_date.strftime("%b %d, %Y") if job.end_date != None else ""
    form.volunteer.data = job.volunteer
    return render_template("edit_jobs.html", form=form)

@app.route('/edit/achievement/<int:id>', methods=["GET", 'POST'])
def edit_achievements(id):
    achievement = Achievement.query.filter_by(id=id).first_or_404()
    if achievement.winner != current_user:
        abort(403)
    form = AddAchievementForm()
    if form.validate_on_submit():
        achievement.name = form.name.data
        achievement.description = form.description.data
        achievement.year = form.year.data
        db.session.commit()
        flash('Your changes have been made.', 'success')
        return redirect(url_for('home'))
    form.name.data = achievement.name
    form.description.data = achievement.description
    form.year.data = achievement.year
    return render_template('edit_achievements.html', form=form)


@app.route('/test')
def test():
    return render_template('test.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


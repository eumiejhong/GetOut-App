from models import bcrypt, User, RecreationGovSite, LikedSite, Story, Comment
from flask_debugtoolbar import DebugToolbarExtension
from db import db, connect_db
from flask import Flask, render_template, request, redirect, flash, session, g, jsonify
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
import datetime
import os
from api import get_campsites, get_rec_parks, DEFAULT_LATITUDE, DEFAULT_LONGITUDE
from forms import SignUpForm, LoginForm, UserEditForm, StoryForm
import json

app = Flask(__name__)
migrate = Migrate(app, db)
env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
app.config.from_object(env_config)

debug = DebugToolbarExtension(app)
migrate = Migrate(app, db)

connect_db(app)

#USER SIGN-UP/LOGIN
#*****************************************************************************************

CURR_USER = 'curr_user'

@app.before_request
def add_user_to_global():
    """If logged in, add user to Flask global"""
    
    if CURR_USER in session:
        g.user = User.query.get(session[CURR_USER])
    else:
        g.user = None

def g_login(user):
    """Logs in the user"""
    
    session[CURR_USER] = user.id

def g_logout():
    """Logs out the user"""

    if CURR_USER in session:
        del session[CURR_USER]

@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    """Shows and handles sign up form"""
    form = SignUpForm()
    if form.validate_on_submit():
        try:
            user = User.signup(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                email=form.email.data,
                city=form.city.data,
                state=form.state.data,
                password=form.password.data,
                image_url=form.image_url.data or User.image_url.default.arg
            )
            db.session.commit()
        except IntegrityError:
            flash('Username already taken', 'danger')
        g_login(user)
        
        return redirect('/')
    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Shows login form"""
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            g_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect('/')
        flash("Invalid credentials!", "danger")
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Handles user logout"""
    session.pop(CURR_USER)
    return redirect('/login')



#USER DETAILS
#****************************************************************************************

@app.route('/user/<int:user_id>')
def user_profile(user_id):
    """Shows user profile"""
    user = User.query.get_or_404(user_id)
    stories = (Story.query.filter(Story.user_id == user_id).order_by(Story.timestamp.desc()).limit(50).all())
    return render_template('user-profile.html', user=user, stories=stories)

@app.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_profile(user_id):
    """Edits user profile"""
    if not g.user:
        flash("Access denied!", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    form = UserEditForm(obj=user)

    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            user.email = form.email.data
            user.city = form.email.data
            user.state = form.state.data
            user.image_url = form.image_url.data
            user.bio = form.bio.data

            db.session.commit()
            return redirect(f'/user/{user.id}')
    return render_template('edit-user-form.html', form=form)

@app.route('/user/delete', methods=['GET'])
def delete_user():
    if not g.user:
        flash("Access unauthorized!", "danger")
        return redirect("/")

    g_logout()

    db.session.delete(g.user)
    db.session.commit()
    return redirect("/sign-up")

#SHOW REC PARKS AND CAMPSITES
#****************************************************************************************

@app.route('/', methods=['GET'])
def show_all_places():
    """Returns locations based on user's location radius"""
    user_latitude = request.args.get('lat', DEFAULT_LATITUDE)
    user_longitude = request.args.get('long', DEFAULT_LONGITUDE)
    radius = request.args.get('radius', None)
    campsites = get_campsites(latitude=user_latitude, longitude=user_longitude, limit=50, radius=radius)
    rec_parks = get_rec_parks(latitude=user_latitude, longitude=user_longitude, limit=50, radius=radius)
    
    site_lists = [campsites, rec_parks]
    for site_list in site_lists:
        for site in site_list:
            print("site.id", site.id)
            existing_model = RecreationGovSite.query.filter_by(id=site.id).first()
            if not existing_model:
                db.session.add(RecreationGovSite(
                    id = site.id,
                    rec_gov_id = site.rec_gov_id,
                    type = site.type,
                    name = site.name,
                    directions = site.directions,
                    city = site.city,
                    state = site.state,
                    latitude = site.latitude,
                    longitude = site.longitude,
                    image_url = site.image_url,
                ))

    db.session.commit()

    render_params = {
        "campsites": campsites,
        "rec_parks": rec_parks,
        "params": request.args
    }
    pageData = {
        "userID": g.user.id if g.user else None,
        "campsites": [c.to_json(g.user) for c in campsites],
        "rec_parks": [c.to_json(g.user) for c in rec_parks],
        "params": {
            "latitude": user_latitude,
            "longitude": user_longitude,
            "radius": radius
        }
    }
    return render_template('locations.html', **render_params, pageData=json.dumps(pageData))

@app.route('/api', methods=['GET'])
def show_all_places_json():
    """Returns locations based on user's location radius"""
    user_latitude = request.args.get('lat', DEFAULT_LATITUDE)
    user_longitude = request.args.get('long', DEFAULT_LONGITUDE)
    radius = request.args.get('radius', None)
    campsites = get_campsites(latitude=user_latitude, longitude=user_longitude, limit=50, radius=radius)
    rec_parks = get_rec_parks(latitude=user_latitude, longitude=user_longitude, limit=50, radius=radius)
    
    site_lists = [campsites, rec_parks]
    for site_list in site_lists:
        for site in site_list:
            existing_model = RecreationGovSite.query.filter_by(id=site.id).first()
            if not existing_model:
                db.session.add(RecreationGovSite(
                    id = site.id,
                    rec_gov_id = site.rec_gov_id,
                    name = site.name,
                    directions = site.directions,
                    city = site.city,
                    state = site.state,
                    latitude = site.latitude,
                    longitude = site.longitude,
                    image_url = site.image_url,
                    type = site.type
                ))

    db.session.commit()

    pageData = {
        "campsites": [c.to_json(g.user) for c in site_lists[0]],
        "rec_parks": [c.to_json(g.user) for c in site_lists[1]],
        "params": {
            "latitude": user_latitude,
            "longitude": user_longitude,
            "radius": radius
        }
    }
    return jsonify(pageData)



#USER LIKE PLACES
#*******************************************************************************************************

@app.route('/site/<action>/<site_id>', methods=['POST'])
def like_action_site(site_id, action):
    """Like/Unlike a site"""

    site = RecreationGovSite.query.filter_by(id = site_id).first_or_404()
    liked_site = LikedSite.query.filter_by(rec_gov_id = site_id).first()

    if not liked_site:
        if action == 'like':
            if not g.user:
                flash("You need to be logged in to do that!", "danger")
                return redirect('/')
            liked_site = LikedSite(rec_gov_id = site.id, user_id = g.user.id, name = site.name, type=site.type)
            db.session.add(liked_site)
            db.session.commit()
    else:
        if action == 'unlike':
            if not g.user:
                flash("You need to be logged in to do that!", "danger")
                return redirect('/')
            db.session.delete(liked_site)
            db.session.commit()

    return {'message': 'Completed!'}


#STORIES
#***********************************************************************************
    
@app.route('/site/<site_id>/add-story', methods=['GET', 'POST'])
def add_story(site_id):
    """Adds campsite user story"""
    if not g.user:
        flash("You need to be logged in to do that!", "danger")
        return redirect('/')
    form = StoryForm()
    site = RecreationGovSite.query.filter_by(id = site_id).first()
    liked_site = LikedSite.query.filter_by(rec_gov_id = site_id).first_or_404()

    if 'rec_park' in site.id: 
        site.type = 'rec_park'
    else:
        site.type = 'campsite'

    if form.validate_on_submit():
        story = Story(
            title = form.title.data,
            content = form.content.data,
            rec_gov_id = site.id,
            user_id = g.user.id,
            liked_site_id = liked_site.id,
            type = site.type
        )
        db.session.add(story)
        db.session.commit()

        return redirect(f"/site/{story.id}/show-story")
    return render_template('story-form.html', form=form, site=site)


@app.route('/site/<site_id>/site-stories')
def show_stories_per_site(site_id):
    site = RecreationGovSite.query.filter_by(id=site_id).first_or_404()
    stories = Story.query.filter_by(rec_gov_id=site_id).all()
    return render_template('show-site-info.html', stories=stories, site=site)


@app.route('/site/<story_id>/show-story', methods=['GET', 'POST'])
def show_story(story_id):
    """Shows user story"""
    story = Story.query.filter_by(id = story_id).first()
    return render_template('story-detail.html', story=story)


@app.route('/site/<story_id>/edit-story', methods=['GET', 'POST'])
def edit_story(story_id):
    """Edits user story"""
    if not g.user:
        flash("You must be logged in to do that!", "danger")
        return redirect("/")

    story = Story.query.get_or_404(story_id)
    form = StoryForm(obj=story)

    if form.validate_on_submit():
        story.title = form.title.data
        story.content = form.content.data
        rec_gov_id = story.rec_gov_id,
        user_id = g.user.id,
        liked_site_id = story.liked_site_id,
        type = story.type
    return render_template('story-form.html', form=form)


#USER COMMENTS
#**************************************************************************************

@app.route('/site/<story_id>/add-comment', methods=['POST'])
def add_comment(story_id):
    """Adds user comment to a campsite story"""

    if not g.user:
        flash('You must log in or sign up to comment!')
        return redirect('/')

    story = Story.query.get_or_404(story_id)
    data = request.json
    if not data['body']:
        flash('You must put a comment body')
        return redirect('/')

    comment = Comment(
        body = data['body'],
        story_id = story.id,
        user_id = story.user_id
    )
    db.session.add(comment)
    db.session.commit()

    comment_serialized = {
        "body": data['body'],
        "story_id": story.id,
        "timestamp": comment.timestamp.strftime('%d %B %Y'),
        "username": g.user.username
    }
    
    return (jsonify(comment=comment_serialized), 201)

@app.route('/site/<story_id>/show-comments')
def show_campsite_comments(story_id):
    """Show all comments for the campsite story"""

    def to_dict(comment): 
        return {
            "body": comment.body,
            "campsite_story_id": comment.story_id,
            "timestamp": comment.timestamp.strftime('%d %B %Y'),
            "username": g.user.username
        }
    comments = [to_dict(comment) for comment in Comment.query.filter_by(story_id=story_id).all()]

    return jsonify(comments=comments)

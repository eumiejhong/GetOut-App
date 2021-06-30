from flask_migrate import Migrate
from db import db
from datetime import datetime
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    password = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, default="https://images.pexels.com/photos/2422265/pexels-photo-2422265.jpeg")
    bio = db.Column(db.Text)
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    stories = db.relationship('Story', backref='user')
    liked_sites = db.relationship('LikedSite', backref='user')


#User like site **************************************************************************************************

    def like_site(self, site):
        if not self.has_liked_site(site):
            like = LikedSite(user_id=self.id, rec_gov_id=site.id, name=site.name)
            db.session.add(like)

    def unlike_site(self, site):
        if self.has_liked_site(site):
            LikedSite.query.filter_by(
                user_id=self.id,
                rec_gov_id = site.id).delete()

    def has_liked_site(self, site):
        return LikedSite.query.filter(
            LikedSite.user_id == self.id,
            LikedSite.rec_gov_id == site.id).first()

#User sign up/authenticate **************************************************************************************

    @classmethod
    def signup(cls, first_name, last_name, username, email, city, state, password, image_url):
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            city=city,
            state=state,
            password=hashed_pwd,
            image_url=image_url
        )
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False

#Rec Gov Site *************************************************************************************************

class RecreationGovSite(db.Model):
    __tablename__ = 'recreation_gov_sites'
    id = db.Column(db.Text, primary_key=True)
    rec_gov_id = db.Column(db.Text)
    type = db.Column(db.Text)
    name = db.Column(db.Text, nullable=False)
    directions = db.Column(db.Text)
    city = db.Column(db.Text)
    state = db.Column(db.Text)
    latitude = db.Column(db.Integer)
    longitude = db.Column(db.Integer)
    image_url = db.Column(db.Text)
    liked_site = db.relationship('LikedSite', backref='gov_site')
    stories = db.relationship('Story', backref='gov_site')

class LikedSite(db.Model):
    __tablename__ = "liked_sites"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rec_gov_id = db.Column(db.Text, db.ForeignKey('recreation_gov_sites.id', ondelete='cascade'))
    name = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    type = db.Column(db.Text)
    story = db.relationship('Story', backref='liked_site')
    
class Story(db.Model):
    __tablename__ = "stories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    liked_site_id = db.Column(db.Integer, db.ForeignKey('liked_sites.id', ondelete='cascade'))
    rec_gov_id = db.Column(db.Text, db.ForeignKey('recreation_gov_sites.id', ondelete='cascade'))
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    type = db.Column(db.Text)
    comments = db.relationship('Comment', backref='story')

class Comment(db.Model):
    __tablename__ = "story_comments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id', ondelete='cascade'))
    body = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('User', backref='campsite_comment')

from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from config import db

class User(db.Model, SerializerMixin):
    __tablename__ = "users"
    serialize_rules = ('-password', '-passengers.user')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    profile = db.relationship('Profile', back_populates='user')
    preferences = db.relationship('Preference', back_populates='user')
    matches = db.relationship('Match', foreign_keys='Match.user_id', back_populates='user')
    potential_matches = db.relationship('Match', foreign_keys='Match.potential_match_id', back_populates='potential_match')    
    likes = db.relationship('Likes', back_populates='user', foreign_keys='Likes.user_id')
    messages = db.relationship('Message', back_populates='user', foreign_keys='Message.user_id')
    blocked = db.relationship('Blocked', back_populates='user', foreign_keys="[Blocked.user_id]")
    
    def __repr__(self):
        return f'<User {self.name}>'
    
class Profile(db.Model, SerializerMixin):
    __tablename__ = "profiles"
    serialize_rules = ('-user',)
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    address = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    bio = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String, nullable=False)
    profile_picture_id = db.Column(db.String, nullable=True)  
    location = db.Column(db.String, nullable=False)
   
    user = db.relationship('User', back_populates='profile') 

    def __repr__(self):
        return f'<Profile {self.user_id}>'
    
class Preference(db.Model, SerializerMixin):
    __tablename__ = "preferences"
    serialize_rules = ('-user', '-preferences.user')
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    preferred_age_min = db.Column(db.Integer, nullable=False)
    preferred_age_max = db.Column(db.Integer, nullable=False)
    preferred_gender = db.Column(db.String, nullable=False)
    preferred_location = db.Column(db.String, nullable=False)
    
    user = db.relationship('User', back_populates='preferences')

    def __repr__(self):
        return f'<Preference {self.user_id}>'
    
class Match(db.Model, SerializerMixin):
    __tablename__ = "matches"
    serialize_rules = ('-user', '-matches.user')
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    potential_match_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String, nullable=False)
    
    user = db.relationship('User', foreign_keys=[user_id], back_populates='matches')
    potential_match = db.relationship('User', foreign_keys=[potential_match_id], back_populates='potential_matches')
    def __repr__(self):
        return f'<Match {self.user_id} - {self.potential_match_id}>'
    
class Likes(db.Model, SerializerMixin):
    __tablename__ = "likes"
    serialize_rules = ('-user', '-likes.user')
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    liked_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User', back_populates='likes', foreign_keys=[user_id])
    liked_user = db.relationship('User', backref='likes_as_liked_user', foreign_keys=[liked_user_id])

    def __repr__(self):
        return f'<Like {self.user_id} - {self.liked_user_id}>'
    
class Message(db.Model, SerializerMixin):
    __tablename__ = "messages"
    serialize_rules = ('-user', '-messages.user')
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    user = db.relationship('User', back_populates='messages', foreign_keys=[user_id])
    recipient = db.relationship('User', backref='messages_as_recipient', foreign_keys=[recipient_id])

    def __repr__(self):
        return f'<Message {self.user_id} - {self.recipient_id}>'

class Blocked(db.Model, SerializerMixin):
    __tablename__ = "blocked"
    serialize_rules = ('-user', '-blocked.user')
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    blocked_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
 
    user = db.relationship('User', back_populates='blocked', foreign_keys=[user_id])
    blocked_user = db.relationship('User', backref='blocked_as_blocked_user', foreign_keys=[blocked_user_id])

    def __repr__(self):
        return f'<Blocked {self.user_id} - {self.blocked_user_id}>'
    
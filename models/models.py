#imports
from mongoengine import Document, StringField, DateTimeField, ListField, ReferenceField
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
import jwt
from config import SECRET_KEY

bcrypt = Bcrypt()

# yorum modeli
class CommentModel(Document):
    user = StringField(required=True)
    comment = StringField(required=True)
    date = DateTimeField(default=datetime.utcnow)

    @property
    def id(self):
        return str(self.pk)

    def to_dict(self):
        return {
            "user": self.user,
            "comment": self.comment,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S"),
        }

# kullanıcı modeli
class UserModel(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    name = StringField(required=True)
    surname = StringField(required=True)
    birthdate = StringField(required=True)
    gender = StringField(required=True)
    profile_image = StringField(required=True)

    @property
    def user_id(self):
        return str(self.id)

    @property
    def token(self):
        payload = {
            "user_id": str(self.id),
            "exp": datetime.utcnow() + timedelta(days=1),
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    def to_dict(self):
        return {
            "_id": str(self.id),
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "name": self.name,
            "surname": self.surname,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "profile_image": self.profile_image,
        }

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, input_password):
        return bcrypt.check_password_hash(self.password, input_password)

# post modeli
class PostModel(Document):
    author = ReferenceField(UserModel, required=True)
    date = DateTimeField(default=datetime.utcnow)
    title = StringField(required=True)
    content = StringField(required=True)
    comments = ListField(ReferenceField(CommentModel))
    votes = ListField(ReferenceField('VoteModel'))

    @property
    def id(self):
        return str(self.pk)

    def to_dict(self):
        comment_list = [comment.to_dict() for comment in self.comments]

        author_user = self.author
        author_username = author_user.username if author_user else "Unknown"

        votes_debug = []
        for vote in self.votes:
            try:
                vote_dict = vote.to_dict()
                votes_debug.append(vote_dict)
            except Exception as e:
                votes_debug.append({"error": str(e), "vote_object": str(vote)})

        return {
            "_id": str(self.pk),
            "author": {
                "_id": str(self.author),
                "username": author_username,
            },
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S"),
            "title": self.title,
            "content": self.content,
            "comments": comment_list,
            "votes": votes_debug,
        }

# oylama modeli
class VoteModel(Document):
    user = ReferenceField(UserModel, required=True)
    post = ReferenceField(PostModel, required=True)
    vote_type = StringField(choices=["upvote", "downvote"], required=True)
    date = DateTimeField(default=datetime.utcnow)
    
    def to_dict(self):
        
        return {
        "user": str(self.user.id),  # str(self.user.id) == self.user.user_id (property)
        "vote_type": self.vote_type,
        "post": str(self.post.id),
        "date": self.date.strftime("%Y-%m-%d %H:%M:%S")
    }

from mongoengine import Document, StringField
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
from config import SECRET_KEY

bcrypt = Bcrypt()


# kullanıcı bilgileri için model
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
    def id(self):
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

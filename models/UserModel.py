from bson import ObjectId
import hashlib
import jwt
from datetime import datetime, timedelta


# kullanıcı bilgileri için model
class UserModel(object):
    def __init__(self, **kwargs):
        if "_id" in kwargs:
            self._id = kwargs["_id"]
        else:
            self._id = ObjectId()

        self.username = kwargs.get("username", "")
        self.email = kwargs.get("email", "")
        self.password = kwargs.get("password", "")
        self.name = kwargs.get("name", "")
        self.surname = kwargs.get("surname", "")
        self.birthdate = kwargs.get("birthdate", "")
        self.gender = kwargs.get("gender", "")
        self.profile_image = kwargs.get("profile_image", "")

    #
    @property
    def id(self):
        return str(self._id)

    @property
    # kullanıcıya özel token oluşturma
    def token(self):
        payload = {
            "user_id": str(self._id),
            "exp": datetime.utcnow() + timedelta(days=1),
        }
        return jwt.encode(payload, "your-secret-key", algorithm="HS256")

    def to_dict(self):
        return {
            "_id": str(self._id),
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "name": self.name,
            "surname": self.surname,
            "birthdate": self.birthdate,
            "gender": self.gender,
            "profile_image": self.profile_image,
        }

    def check_password(self, input_password):
        return (
            self.password == hashlib.sha256(input_password.encode()).hexdigest()
        )  # şifre için hashleme işlemi yapılıyor ve karşılaştırılıyor

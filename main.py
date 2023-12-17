from flask import Flask, request, jsonify
from mongoengine import connect
from flask_bcrypt import Bcrypt
from config import MONGODB_CONNECTION_STRING
from models.UserModel import UserModel

app = Flask(__name__)
bcrypt = Bcrypt()

# mongodb bağlantısını config.py dosyasından alıyoruz ve bağlantıyı gerçekleştiriyoruz.
db = connect("my_database", host=MONGODB_CONNECTION_STRING)


# kayıt olma fonksiyonu
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")
    surname = data.get("surname")
    birthdate = data.get("birthdate")
    gender = data.get("gender")
    profile_image_url = data.get("profile_image_url")

    # kullanıcı kontrolü
    existing_user = UserModel.objects(username=username).first()
    if existing_user:
        return jsonify({"message": "Kullanıcı adı zaten alınmış."}), 400

    new_user = UserModel(
        username=username,
        email=email,
        name=name,
        surname=surname,
        birthdate=birthdate,
        gender=gender,
        profile_image=profile_image_url,
    )
    new_user.set_password(password)
    new_user.save()

    return jsonify({"message": "Kayıt başarılı."}), 201


# giriş yapma fonksiyonu
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # kullanıcı adı ve şifre kontrolü
    user = UserModel.objects(username=username).first()
    if user and user.check_password(password):
        return jsonify({"message": "Giriş başarılı", "token": user.token}), 200
    else:
        return jsonify({"message": "Kullanıcı adı veya şifre yanlış."}), 401


@app.route("/users", methods=["GET"])
def get_users():
    users = UserModel.objects().all()
    user_list = [user.to_dict() for user in users]
    return jsonify({"users": user_list})


if __name__ == "__main__":
    app.run(debug=True)

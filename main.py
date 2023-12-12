import pymongo
from models.UserModel import UserModel
import jwt
from datetime import datetime, timedelta

## mongodb bağlantı bilgileri
MONGODB_CONNECTION_STRING = "mongodb+srv://berkayozgun:uNjNgCPGHv74gD7q@microblog-cluster.wnxotnz.mongodb.net/?retryWrites=true&w=majority"

# mongodb bağlantısı
client = pymongo.MongoClient(MONGODB_CONNECTION_STRING)
db = client["my_database"]

try:
    # bağlantı testi
    client.admin.command("ismaster")
except pymongo.errors.ConnectionFailure as e:
    print(f"Bağlantı başarısız: {e}")
    exit()

db = client["my_database"]


# kayıt olma fonksiyonu
def register():
    username = input("Kullanıcı adı: ")
    email = input("E-posta adresi: ")
    password = input("Şifre: ")
    name = input("Ad: ")
    surname = input("Soyad: ")
    birthdate = input("Doğum tarihi (YYYY-MM-DD): ")
    gender = input("Cinsiyet (male/female): ")
    profile_image_url = input("Profil resmi URL'si: ")

    # kullanıcı adı kontrolü
    existing_user = db["users"].find_one({"username": username})
    if existing_user:
        print("Bu kullanıcı adı zaten kullanımda.")
    else:
        user = UserModel(
            username=username,
            email=email,
            password=password,
            name=name,
            surname=surname,
            birthdate=birthdate,
            gender=gender,
            profile_image=profile_image_url,
        )
        db["users"].insert_one(user.to_dict())
        print("Kayıt başarılı.")


# giriş yapma fonksiyonu


def login():
    username = input("Kullanıcı adı: ")
    password = input("Şifre: ")

    # kullanıcı adı ve şifre kontrolü
    user = db["users"].find_one({"username": username})
    if user and UserModel(**user).check_password(password):
        user_obj = UserModel(**user)
        token = user_obj.token
        print("Giriş başarılı.")
        print("jwt Token:", token)
    else:
        print("Kullanıcı adı veya şifre hatalı.")


# giriş menüsü
while True:
    print("1. Register\n2. Login\n3. Exit")
    choice = input("Seçiminizi yapın: ")

    if choice == "1":
        register()
    elif choice == "2":
        login()
    elif choice == "3":
        break
    else:
        print("Geçersiz seçenek.")

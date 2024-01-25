#imports
from datetime import datetime
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    verify_jwt_in_request,
    current_user,
    unset_jwt_cookies,
)
from mongoengine import connect
from flask_bcrypt import Bcrypt
from config import MONGODB_CONNECTION_STRING, SECRET_KEY
from models.models import UserModel, PostModel, CommentModel, VoteModel
from bson import ObjectId
from bson.errors import InvalidId
from flask_cors import CORS

# flask uygulamasını oluşturuyoruz. 
# JWT_SECRET_KEY değerini config.py dosyasından alıyoruz. 
# JWTManager ile JWT kimlik doğrulaması yapabilmek için JWTManager nesnesi oluşturuyoruz.
# Bcrypt ile şifreleme yapabilmek için Bcrypt nesnesi oluşturuyoruz.
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = SECRET_KEY
jwt = JWTManager(app)
bcrypt = Bcrypt()
CORS(app, supports_credentials=True)

# mongodb bağlantısını gerçekleştiriyoruz.
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

    access_token = create_access_token(identity=str(new_user.id))
    return jsonify({"message": "Kayıt başarılı.", "access_token": access_token}), 201


# giriş yapma fonksiyonu
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # kullanıcı adı ve şifre kontrolü
    user = UserModel.objects(username=username).first()
    if user and user.check_password(password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({
            "message": "Giriş başarılı",
            "access_token": access_token,
            "username": user.username
            }), 200
    else:
        return jsonify({"message": "Kullanıcı adı veya şifre yanlış."}), 401


# kayıtlı kullanıcıları listeleme fonksiyonu
# kayıtlı kullanıcıları listeleme fonksiyonu
@app.route("/users", methods=["GET"])
def get_users():
    users = UserModel.objects().all()
    user_list = [user.to_dict() for user in users]
    return jsonify({"users": user_list})


# post oluşturma fonksiyonu
@app.route("/create_post", methods=["POST"])
@jwt_required()
def create_post():
    data = request.get_json()
    author_id = get_jwt_identity()
    title = data.get("title")
    content = data.get("content")

    author = UserModel.objects(id=author_id).first()

    if not author:
        return jsonify({"message": "Kullanıcı bulunamadı."}), 404

    new_post = PostModel(author=author_id, title=title, content=content)
    new_post.save()

    return (
        jsonify({"message": "Post başarıyla oluşturuldu.", "post": new_post.to_dict()}),
        201,
    )

# authenticated kullanıcı bilgilerini getirme fonksiyonu
@app.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()

    try:
        user = UserModel.objects(id=user_id).first()
    except:
        return jsonify({"message": "Kullanıcı bulunamadı."}), 404
    
    if user:
        return jsonify({
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "surname": user.surname
            }), 200
    else:
        return jsonify({"message": "Kullanıcı bulunamadı."}), 404
        


# belli bir kullanıcının postlarını listeleme fonksiyonu
@app.route("/user_posts", methods=["GET"])
def get_user_posts():
    verify_jwt_in_request()
    author = get_jwt_identity()
    posts = PostModel.objects(author=author).all()
    post_list = [post.to_dict() for post in posts]
    return jsonify({"posts": post_list})


# belirli bir postu görüntüleme fonksiyonu
@app.route("/posts/<post_id>", methods=["GET"])
def get_post(post_id):
    post = PostModel.objects(id=post_id).first()
    if post:
        post_dict = post.to_dict()
        post_dict["_id"] = str(post_dict["_id"])
        return jsonify({"post": post.to_dict()}), 200
    else:
        return jsonify({"message": "Post bulunamadı."}), 404


# belirli bir post'u silme fonksiyonu
@app.route("/post/<post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    current_user = get_jwt_identity()
    post = PostModel.objects(id=post_id, author=current_user).first()

    if post:
        post.delete()
        return jsonify({"message": "Post başarıyla silindi."}), 200
    else:
        return jsonify({"message": "Post bulunamadı veya silme izni yok"}), 404


# JWT kimliğini kullanarak MongoDB'den kullanıcı nesnesini çeken işlev
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    print(f"identity: {identity}")

    try:
        user_id = ObjectId(identity)
        print(f"user_id: {user_id}")
    except InvalidId:
        print("User id is not valid")
        return None
    except Exception as e:
        print("An error occurred", e)
        return None

    user = UserModel.objects(id=user_id).first()

    if user:
        return user
    else:
        print("User not found for id: {user_id}")
        return None


# yorum ekleme fonksiyonu
@app.route("/add_comment/<post_id>", methods=["POST"])
@jwt_required()
def add_comment(post_id):
    data = request.get_json()
    comment_content = data.get("content")

    if not comment_content:
        return jsonify({"message": "Yorum içeriği boş olamaz."}), 400

    try:
        post = PostModel.objects.get(pk=post_id)
    except:
        return jsonify({"message": "Post bulunamadı."}), 404

    user_id = str(current_user.id)

    comment = CommentModel(
        user=user_id, comment=comment_content, date=datetime.utcnow()
    )
    comment.save()
    post.comments.append(comment)
    post.save()

    return jsonify({"message": "Yorum başarıyla eklendi.", "post": post.to_dict()}), 201



# bütün kullanıcıların postlarını listeleme fonksiyonu
@app.route("/all_posts", methods=["GET"])
def get_all_posts():
    print("Inside get_all_posts function")  # Debug çıktısı ekle
    posts = PostModel.objects().all()
    print("Posts retrieved successfully")  # Debug çıktısı ekle
    post_list = []

    for post in posts:
        post_dict = post.to_dict()
        post_dict["_id"] = str(post_dict["_id"])

        # Yorumların içindeki user alanını güncelle
        for comment in post_dict["comments"]:
            comment_user_id = comment["user"]
            comment_user = UserModel.objects(id=comment_user_id).first()
            if comment_user:
                comment["user"] = comment_user.username

        post_list.append(post_dict)

    print("Posts converted to dictionary successfully")  # Debug çıktısı ekle

    return jsonify({"posts": post_list})



# posta oy verme fonksiyonu
@app.route("/vote/<post_id>", methods=["POST"])
@jwt_required()
def vote(post_id):
    data = request.get_json()
    vote_type = data.get("vote_type")

    if vote_type not in ["upvote", "downvote"]:
        return jsonify({"message": "Geçersiz oy tipi."}), 400

    post = PostModel.objects(id=post_id).first()

    if not post:
        return jsonify({"message": "Post bulunamadı."}), 404

    user_id = str(current_user.id)

    existing_vote = VoteModel.objects(user=user_id, post=post).first()

    if existing_vote:
        return jsonify({"message": "Zaten oy kullandınız."}), 400

    new_vote = VoteModel(user=current_user, post=post, vote_type=vote_type)
    new_vote.save()

    post.votes.append(new_vote)
    post.save()

    return jsonify({"message": "Oy başarıyla eklendi.", "post": post.to_dict()}), 201


#çıkış yapma fonksiyonu
@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():

    current_user_id = get_jwt_identity()
    print(f"current_user_id: {current_user_id}")

    response = jsonify({"message": "Çıkış başarılı."})
    unset_jwt_cookies(response)
    return response, 200



if __name__ == "__main__":
    app.run(debug=True)

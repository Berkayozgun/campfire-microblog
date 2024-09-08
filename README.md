# campfire-microblog

Twitter-like micro blogging platform, where users can create, read, comment or vote posts.

## Description

This project serves as a backend for campfire project. It is implemented using Flask, a lightweight web framework for Python.

## Getting Started

Follow the steps below to set up and run the Flask backend on your local machine.

### Installation

1. Clone the project to your local machine.

   ```bash
   git clone https://github.com/Berkayozgun/campfire_microblog-microblog.git

   ```

2. Navigate to the project folder.

   ```bash
   cd campfire_microblog-microblog.git

   ```

3. Navigate to the latest upgraded branch

   ```bash
   git checkout feature/logout

   ```

4. Install the dependencies

   ```bash
   pip install -r requirements.txt

   ```

5. Start the backend of app
   ```bash
   python main.py
   ```

## Configuration

Make sure you have a MongoDB instance running and update the MONGODB_CONNECTION_STRING and SECRET_KEY values in the config.py file.

### API Usage

#### Registration

##### Endpoint: `/register`

##### Method: `POST`

###### Body:

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "123456",
  "name": "John",
  "surname": "Doe",
  "birthdate": "1990-01-01",
  "gender": "male",
  "profile_image_url": "https://example.com/profile.jpg"
}
```

###### Response:

```json
{
  "message": "Kayıt başarılı.",
  "access_token": "jwt_token"
}
```

#### Login

##### Endpoint: `/login`

##### Method: `POST`

###### Body:

```json
{
  "username": "testuser",
  "password": "123456"
}
```

###### Response:

```json
{
  "message": "Giriş başarılı",
  "access_token": "jwt_token",
  "username": "testuser"
}
```

#### Get User Profile

##### Endpoint: `/profile`

##### Method: `GET`(Requires JWT token)

###### Response:

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "name": "John",
  "surname": "Doe"
}
```

#### Create Post

##### Endpoint: `/create_post`

##### Method: `POST`(Requires JWT token)

###### Body:

```json
{
  "title": "First Post",
  "content": "This is my first post"
}
```

###### Response:

```json
{
  "message": "Post başarıyla oluşturuldu.",
  "post": {
    "title": "First Post",
    "content": "This is my first post"
  }
}
```

#### Get User Posts

##### Endpoint: `/user_posts`

##### Method: `GET`(Requires JWT token)

###### Response:

```json
{
  "posts": [
    {
      "title": "First Post",
      "content": "This is my first post"
    }
  ]
}
```

#### Get All Posts

##### Endpoint: `/all_posts`

##### Method: `GET`

###### Response:

```json
{
  "posts": [
    {
      "title": "First Post",
      "content": "This is my first post"
    }
  ]
}
```

#### Comment on Post

##### Endpoint: `/add_comment/<post_id>`

##### Method: `POST`(Requires JWT token)

###### Body:

```json
{
  "content": "This is a comment"
}
```

###### Response:

```json
{
  "message": "Yorum başarıyla eklendi.",
  "post": {
    "title": "First Post",
    "comments": [
      {
        "user": "testuser",
        "comment": "Great post!"
      }
    ]
  }
}
```

#### Vote on a Post

##### Endpoint: `/vote/<post_id>``

##### Method: `POST`(Requires JWT token)

###### Body:

```json
{
  "vote_type": "upvote"
}
```

###### Response:

```json
{
  "message": "Oy başarıyla eklendi.",
  "post": {
    "title": "First Post",
    "votes": [
      {
        "user": "testuser",
        "vote_type": "upvote"
      }
    ]
  }
}
```

## Get Post by ID

##### Endpoint: `/posts/<post_id>``

##### Method: `GET`

###### Response:

```json
{
  "post": {
    "title": "First Post",
    "content": "This is my first post"
  }
}
```

## Delete Post

##### Endpoint: `/post/<post_id>``

##### Method: `DELETE`(Requires JWT token)

###### Response:

```json
{
  "message": "Post successfully deleted."
}
```

## Logout

##### Endpoint: `/logout`

##### Method: `POST`(Requires JWT token)

###### Response:

```json
{
  "message": "Logout successful."
}
```

# Models

## UserModel

```
- username (String) : Unique username of the user.
- email (String) : Unique email address of the user.
- name (String) : Name of the user.
- surname (String) : Surname of the user.
- birthdate (String) : Birthdate of the user.
- gender (String) : Users's gender
- profile_image (String) : URL of the user's profile image.
```

## PostModel

```
- author (Reference) : Reference to the user who created the post.
- date (DateTime) : Date and time of the post creation.
- title (String) : Title of the post.
- content (String) : Content of the post.
- comments (List) : List of comments on the post.
- votes (List) : List of votes on the post.
```

## CommentModel

```
- user (Reference) : Reference to the user who created the comment.
- content (String) : Content of the comment.
- date (DateTime) : Date and time of the comment creation.
```

## VoteModel

```
- user (Reference) : Reference to the user who voted.
- vote_type (String) : Type of the vote (upvote or downvote).
- post (Reference) : Reference to the post that was voted on.
- date (DateTime) : Date and time of the vote.
```

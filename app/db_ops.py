from .models import User

def get_by_username(username):
    return User.objects(username=username).first()

def get_by_email(email):
    return User.objects(email=email).first()

def create_user(first_name, last_name, email, username, password, avatar):
    user = User(first_name=first_name, last_name=last_name, email=email, username=username)
    user.set_password(password)
    user.set_avatar(avatar)
    user.save()

def get_all_users():
    return User.objects()
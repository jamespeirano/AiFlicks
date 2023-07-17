from .models import User

def get_user_by_username(username):
    return User.objects(username=username).first()

def get_user_by_email(email):
    return User.objects(email=email).first()

def save_user(user):
    user.save()
    return user

def create_user(first_name, last_name, email, username, password, avatar):
    user = User(first_name=first_name, last_name=last_name, email=email, username=username)
    user.set_password(password)
    user.set_avatar(avatar)
    user.save()
    return user
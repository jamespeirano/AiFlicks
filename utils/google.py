import requests
import string, random 

__all__ = ['generate_random_password', 'get_google_profile_pic']

def generate_random_password(length=12):
    chars = string.ascii_letters + string.digits + '!@#$%^&*'
    password = ''.join(random.choices(chars, k=length))
    return password

def get_google_profile_pic(pic):
    avatar = requests.get(pic).content
    return avatar
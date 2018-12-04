import os


BASIC_AUTH_USERNAME = os.getenv("USERNAME") or "test"
BASIC_AUTH_PASSWORD  =  os.getenv("PASSWORD") or "password"
SECRET_KEY=os.getenv("SECRET_KEY") or 'try1234'


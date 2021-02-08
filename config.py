import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.urandom(24)
    env = os.environ['DATABASE_URL'] = 'postgres://yycyfqgyyohwrf:1c2693cc568cb74986c58fc95bed0b6108e93614b710070252356a769735477c@ec2-34-198-31-223.compute-1.amazonaws.com:5432/d9vvnc5cts47mn'
    SQLALCHEMY_DATABASE_URI = env
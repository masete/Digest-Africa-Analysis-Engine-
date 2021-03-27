import os
from dotenv import load_dotenv

# basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:13579246@localhost/digestafricadb'
    SQLALCHEMY_DATABASE_URI = 'postgres://ymzgbzaoueezqo:7165a1f63de0e295e496302822684853a5914bef93a0319b8f5d6dc5df' \
                              '459' \
                              '5a9@ec2-54-196-111-158.compute-1.amazonaws.com:5432/d45ndhrceblt7r'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    ADMINS = ["nicholasmasete72@gmail.com"]

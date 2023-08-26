from datetime import timedelta


# 配置文件
class Config:
    SECRET_KEY = "your_secret_key"
    DATABASE_URI = "your_database_uri"

    # google cloud storage 設定
    MY_BUCKET = "my_db_files"
    MY_DATABASE = "users.db"

    # flask-jwt-extended 設定
    JWT_SECRET_KEY = "super-secret"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)

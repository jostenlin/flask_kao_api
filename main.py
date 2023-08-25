# import os
# import subprocess
from flask import Flask
from flask_restful import Api

from auth import AuthRoutes
from config import Config
from users import Users, User

# 動態路由
from asyncRoutes import AsyncRoutes

app = Flask(__name__)

# 允許跨域請求
from flask_cors import CORS

CORS(app)

# 載入設定檔config.py所有設定
# 包括 flask-jwt-extended 的設定
app.config.from_object(Config)

# 設定權限相關路由
AuthRoutes.configure_routes(app)

# 設定其他路由
api = Api(app)
api.add_resource(Users, "/users")
api.add_resource(User, "/user")

api.add_resource(AsyncRoutes, "/getAsyncRoutes")

# from login import Login
# api.add_resource(Login, "/login")


# 測試用路由(可刪除)
@app.route("/")
def hello_world():
    # 讀取config.py的配置
    app.config.from_object("config.Config")
    from flask import current_app

    return {"DEBUG": current_app.config["DEBUG"]}
    # return {"DEBUG": current_app.config["JWT_SECRET_KEY"]}
    # return "hi:" + os.environ.get("DB_URL")


if __name__ == "__main__":
    app.run(debug=True)

    # Mount the Cloud Storage bucket before starting the application
    # my-bucket name = my_db_files
    # os.makedirs("/mnt/my_db_files", exist_ok=True)
    # subprocess.run(["gcsfuse", "my_db_files", "/mnt/my_db_files"])

    # Now the SQLite database file can be accessed at
    # '/mnt/my-bucket/my-database.db'
    # '/mnt/my_db_files/users.db'

    # 在cloud run時，使用環境變量port。
    # 若在本機端測試時找不到，使用預設值port=5000
    # port = int(os.environ.get("PORT", 5000))
    # app.run(debug=True, host="0.0.0.0", port=port)

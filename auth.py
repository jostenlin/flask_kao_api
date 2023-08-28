from datetime import timedelta
import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from flask import Flask, request, jsonify

from flask_jwt_extended import create_access_token, create_refresh_token, JWTManager


class AuthRoutes:
    @staticmethod
    def configure_routes(app):
        # 建立 Flask-JWT-Extended 實例
        JWTManager(app)

        # 登入以取得 JWT Token
        @app.route("/login", methods=["POST"])
        def login():
            # 初始化 Firebase Admin SDK
            cred = credentials.Certificate("./firebase_key.json")
            firebase_admin.initialize_app(cred)

            # 取得使用者傳過來的 JSON
            req = request.get_json()

            # 驗證idtoken
            # email = req.get("email")
            idtoken = req.get("idtoken")

            try:
                # 验证 ID Token
                decoded_token = auth.verify_id_token(idtoken)

                # 如果成功验证，decoded_token 包含用户信息
                user_id = decoded_token["uid"]
                # user_id = "123"
                
                access_token = create_access_token(
                    identity=user_id, expires_delta=timedelta(hours=1)
                )
                refresh_token = create_refresh_token(
                    identity=user_id, expires_delta=timedelta(days=1)
                )
                res = {
                    "success": True,
                    "data": {
                        "username": decoded_token["name"],
                        # "username": "admin",
                        "roles": ["admin"],
                        "accessToken": access_token,
                        "refreshToken": refresh_token,
                        "expires": (
                            timedelta(hours=1) + datetime.datetime.now()
                        ).strftime("%Y/%m/%d %H:%M:%S"),
                        "uid": decoded_token["uid"],
                        "email": decoded_token["email"],
                        "picture": decoded_token["picture"],
                    },
                }
                return res, 200
            except auth.InvalidIdTokenError:
                return jsonify({"error": "Invalid ID Token"}), 401

        # 更新 JWT Token
        @app.route("/refreshtoken", methods=["POST"])
        def refreshtoken():
            # 取得使用者傳過來的 JSON
            req = request.get_json()

            # 取得 refresh token
            refresh_token = req.get("refreshtoken")

            try:
                # 使用 JWT 验证 refresh token
                # 如果成功验证，會返回user_id
                # user_id = get_jwt_identity(refresh_token)
                user_id = "123"
                access_token = create_access_token(
                    identity=user_id, expires_delta=timedelta(hours=1)
                )
                res = {
                    "success": True,
                    "data": {
                        "accessToken": access_token,
                        "refreshToken": refresh_token,
                        "expires": (
                            timedelta(hours=1) + datetime.datetime.now()
                        ).strftime("%Y/%m/%d %H:%M:%S"),
                    },
                }
                return res, 200
            except:
                return {"success": False, "data": {}}, 401

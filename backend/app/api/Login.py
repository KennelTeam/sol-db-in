from flask import request, jsonify, Response
from flask_jwt_extended import create_access_token, set_access_cookies
from flask_restful import Resource

from backend.app.database import User


class Login(Resource):

    @staticmethod
    def post() -> Response:
        login = request.json.get('login')
        password = request.json.get('password')
        if not login or not password:
            return jsonify(message='You should provide login and password'), 400

        user = User.get_by_login(login)
        if not user:
            return jsonify(message='No such user'), 404

        user = user.auth(login, password)
        if not user:
            return jsonify(message='Wrong password'), 401

        user.current_ip = request.remote_addr
        response = jsonify(role=user.role.name)
        access_token = create_access_token(identity=user)
        set_access_cookies(response, access_token)
        return response

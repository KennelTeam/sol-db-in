import os
from datetime import timedelta, datetime, timezone

from flask import redirect, url_for, request, Response
from flask_jwt_extended import JWTManager, get_jwt, create_access_token, set_access_cookies, jwt_required, current_user
from flask_jwt_extended.exceptions import NoAuthorizationError

from .flask_app import FlaskApp
from backend.app.database import User
from ..constants import JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_EXPIRING_TIME

FlaskApp().app.config["JWT_COOKIE_SECURE"] = False
FlaskApp().app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
FlaskApp().app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
FlaskApp().app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=JWT_ACCESS_TOKEN_EXPIRES)
FlaskApp().app.config['JWT_COOKIE_CSRF_PROTECT'] = False
FlaskApp().app.config['PROPAGATE_EXCEPTIONS'] = True

jwt = JWTManager(FlaskApp().app)


@jwt_required()
@FlaskApp().app.after_request
def refresh_expiring_jwts(response) -> Response:
    try:
        if request.endpoint in ('login', 'logout'):
            return response
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=JWT_REFRESH_EXPIRING_TIME))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=current_user)
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError, NoAuthorizationError):
        return redirect(url_for('logout'))


@jwt.user_identity_loader
def user_identity_lookup(user: User) -> str:
    return {'login': user.login, 'current_ip': user.current_ip}


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header: dict, jwt_data: dict) -> User:
    data = jwt_data['sub']
    login = data.get('login')
    current_ip = data.get('current_ip')
    user = User.get_by_login(login)
    user.current_ip = current_ip
    return user

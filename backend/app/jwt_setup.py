import os
from datetime import timedelta, datetime, timezone

from flask import Response, request
from flask_jwt_extended import JWTManager, get_jwt, create_access_token, set_access_cookies, jwt_required, current_user, \
    unset_jwt_cookies

from .api.auxiliary import get_failure, post_failure, HTTPErrorCode
from .flask_app import FlaskApp
from backend.app.database import User
from ..constants import JWT_ACCESS_TOKEN_EXPIRES, JWT_REFRESH_EXPIRING_TIME

FlaskApp().app.config['JWT_COOKIE_SECURE'] = True
FlaskApp().app.config['JWT_COOKIE_SAMESITE'] = "None"
FlaskApp().app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
FlaskApp().app.config['JWT_TOKEN_LOCATION'] = ['cookies']
FlaskApp().app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=JWT_ACCESS_TOKEN_EXPIRES)
FlaskApp().app.config['JWT_COOKIE_CSRF_PROTECT'] = False
FlaskApp().app.config['PROPAGATE_EXCEPTIONS'] = True

jwt = JWTManager(FlaskApp().app)


@jwt_required()
@FlaskApp().app.after_request
def refresh_expiring_jwts(response: Response) -> Response:
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=JWT_REFRESH_EXPIRING_TIME))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=current_user)
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response


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


@jwt.unauthorized_loader
def unauthorized_loader_callback(_reason: str) -> Response:
    if request.method == 'GET':
        response = get_failure(HTTPErrorCode.JWT_NOT_FOUND, 403)
    else:
        response = post_failure(HTTPErrorCode.JWT_NOT_FOUND, 403)
    unset_jwt_cookies(response)
    return response


@jwt.expired_token_loader
def expired_token_loader_callback(_jwt_header: dict, _jwt_payload: dict) -> Response:
    if request.method == 'GET':
        response = get_failure(HTTPErrorCode.JWT_EXPIRED, 401)
    else:
        response = post_failure(HTTPErrorCode.JWT_EXPIRED, 401)
    unset_jwt_cookies(response)
    return response


@jwt.invalid_token_loader
def invalid_token_loader_callback(_reason: str) -> Response:
    if request.method == 'GET':
        response = get_failure(HTTPErrorCode.INVALID_JWT, 403)
    else:
        response = post_failure(HTTPErrorCode.INVALID_JWT, 403)
    unset_jwt_cookies(response)
    return response

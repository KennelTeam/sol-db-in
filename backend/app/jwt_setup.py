import os
from datetime import timedelta, datetime, timezone

from flask import redirect, url_for, request, Response
from flask_jwt_extended import JWTManager, get_jwt, create_access_token, set_access_cookies, jwt_required, current_user, \
    verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError

from .flask_app import FlaskApp
from backend.app.database import User
from ..constants import JWT_ACCESS_TOKEN_EXPIRES

FlaskApp().app.config["JWT_COOKIE_SECURE"] = False
FlaskApp().app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
FlaskApp().app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
FlaskApp().app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=JWT_ACCESS_TOKEN_EXPIRES)
FlaskApp().app.config['JWT_COOKIE_CSRF_PROTECT'] = False
FlaskApp().app.config['PROPAGATE_EXCEPTIONS'] = True

jwt = JWTManager(FlaskApp().app)
# jwt._set_error_handler_callbacks(FlaskApp().api)


# @FlaskApp().api.errorhandler(NoAuthorizationError)
# def handle_auth_error(e):
#     return {'message': str(e)}, 401


# @jwt_required()
# @FlaskApp().app.after_request
# def refresh_expiring_jwts(response) -> Response:
#     try:
#         if request.endpoint == 'login' or request.endpoint == 'register':
#             return response
#         verify_jwt_in_request()
#         exp_timestamp = get_jwt()["exp"]
#         now = datetime.now(timezone.utc)
#         target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
#         if target_timestamp > exp_timestamp:
#             access_token = create_access_token(identity=current_user)
#             set_access_cookies(response, access_token)
#         return response
#     except (RuntimeError, KeyError, NoAuthorizationError):
#         return redirect(url_for('logout'))


@jwt.user_identity_loader
def user_identity_lookup(user: User) -> str:
    return user.login


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header: dict, jwt_data: dict) -> User:
    login = jwt_data["sub"]
    return User.get_by_login(login)

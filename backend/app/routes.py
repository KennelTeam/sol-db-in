#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from .api.login import Login
from .api.logout import Logout
from .api.register import Register
from .api.forms import Forms
from .flask_app import FlaskApp


FlaskApp().api.add_resource(Login, '/login')
FlaskApp().api.add_resource(Register, '/register')
FlaskApp().api.add_resource(Logout, '/logout')
FlaskApp().api.add_resource(Forms, '/forms')

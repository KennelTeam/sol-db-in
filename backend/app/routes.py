#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved.
from .api.Login import Login
from .api.Logout import Logout
from .api.Register import Register
from .flask_app import FlaskApp


FlaskApp().api.add_resource(Login, '/login')
FlaskApp().api.add_resource(Register, '/register')
FlaskApp().api.add_resource(Logout, '/logout')

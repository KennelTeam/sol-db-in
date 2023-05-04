#  Copyright (c) 2020-2023. KennelTeam.
#  All rights reserved
import requests
import json
from tqdm import tqdm

from backend.auxiliary.misc import get_sol_db_logger

from .toponym import Toponym
from backend.constants import TOPONYMS_TABLE_URL, TOPONYMS_REQUEST_TIMEOUT
from backend.app.flask_app import FlaskApp


logger = get_sol_db_logger('flask-server')


def import_toponyms():
    response = requests.get(TOPONYMS_TABLE_URL, timeout=TOPONYMS_REQUEST_TIMEOUT)
    cities = json.loads(
            response.content.decode()
        )

    with FlaskApp().app.app_context():
        indonesia = Toponym("Indonesia")
        FlaskApp().add_database_item(indonesia)
        FlaskApp().flush_to_database()

        names = {city['admin_name'] for city in cities}
        regions = {name: Toponym(name, indonesia.id) for name in names}
        logger.debug('Creating regions...')
        for region in tqdm(regions.values()):
            FlaskApp().add_database_item(region)
        FlaskApp().flush_to_database()
        total_count = len(regions)
        logger.debug('Creating cities...')
        for city in tqdm(cities):
            if city['city'] not in names:
                new_city = Toponym(city['city'], regions[city['admin_name']].id)
                FlaskApp().add_database_item(new_city)
                names.add(city['city'])
                total_count += 1
        FlaskApp().flush_to_database()
        logger.debug('Successfully imported %s toponyms', total_count)

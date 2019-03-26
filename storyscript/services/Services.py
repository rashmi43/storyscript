# -*- coding: utf-8 -*-
import json
from functools import lru_cache

import requests

from .DB import DB


# noinspection PyMethodMayBeStatic
class Services:

    def update(self):
        query = """
        {
          allServiceTags {
            nodes {
              service {
                name
                alias
                owner {
                  username
                }
                topics
                description
                isCertified
                public
              }
              serviceUuid
              state
              configuration
              readme
            }
          }
        }
        """
        res = requests.post('https://api.asyncy.com/graphql',
                            data=json.dumps({
                                'query': query
                            }),
                            headers={'Content-Type': 'application/json'},
                            timeout=10)

        data = res.json()
        services = data['data']['allServiceTags']['nodes']
        with DB() as db:
            with db.atomic(lock_type='IMMEDIATE'):
                DB.Service.delete().execute()
                for service in services:
                    DB.Service.create(
                        service_uuid=service['serviceUuid'],
                        name=service['service']['name'],
                        alias=service['service']['alias'],
                        username=service['service']['owner']['username'],
                        description=service['service']['description'],
                        certified=service['service']['isCertified'],
                        public=service['service']['public'],
                        topics=service['service']['topics'],
                        state=service['state'],
                        configuration=service['configuration'],
                        readme=service['readme'])

    @lru_cache(maxsize=1)
    def get(self, alias=None, owner=None, name=None) -> DB.Service:
        """
        Get a service from the database.

        :param alias: Takes precedence when specified over owner/name
        :param owner: The owner of the service
        :param name: The name of the service
        :return: Returns a DB.Service instance, with all fields selected
        """
        with DB():
            if alias:
                service = DB.Service.select().where(DB.Service.alias == alias)
            else:
                service = DB.Service.select().where(
                    (DB.Service.username == owner) & (DB.Service.name == name))
        return service.get()

    @lru_cache(maxsize=1)
    def get_all_service_names(self) -> [str]:
        """
        Get all service names and aliases from the database.

        :return: An array of strings, which might look like:
        ["hello", "universe/hello"]
        """
        services = []
        with DB():
            for s in DB.Service.select(DB.Service.name, DB.Service.alias,
                                       DB.Service.username):
                if s.alias:
                    services.append(s.alias)

                services.append(f'{s.username}/{s.name}')

        return services


# TODO: convert the following into an integration test
c = Services()
c.update()
s = c.get(alias='python')
print(s.public)
s = c.get(owner='microservice', name='python')
print(s.configuration)
print(c.get_all_service_names())

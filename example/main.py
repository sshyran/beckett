from beckett import clients, resources


class PersonResource(resources.BaseResource):
    class Meta:
        name = 'Person'
        resource_name = 'people'
        identifier = 'url'
        attributes = (
            'name',
            'birth_year',
            'eye_color',
            'gender',
            'height',
            'mass',
            'url',
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )


class StarWarsClient(clients.BaseClient):
    class Meta:
        name = 'Star Wars API Client'
        base_url = 'http://swapi.co/api'
        resources = (
            PersonResource,
        )

swapi = StarWarsClient()
results_list = swapi.get_person(uid=1)
person = results_list[0]
print(person.name)

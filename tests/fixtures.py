# -*- coding: utf-8 -*-

from beckett import clients, resources


class PeopleResource(resources.BaseResource):

    class Meta(resources.BaseResource.Meta):
        name = 'People'
        identifier = 'name'
        attributes = (
            'name',
            'slug',
            'another_thing',
        )
        methods = (
            'get',
            'post',
        )


class PlainTestClient(clients.BaseClient):

    class Meta(clients.BaseClient.Meta):
        name = 'test_client'
        base_url = 'test://dev/api'
        resources = (
            PeopleResource,
        )

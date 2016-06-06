#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_clients
----------------------------------

Tests for `beckett.clients` module.
"""


from .fixtures import PlainTestClient


def test_custom_client():
    """
    Test our own custom client - PlainTestClient
    """
    client = PlainTestClient()
    # Our PlainTestClient should have a registered GET method
    # For the Testy resource
    assert hasattr(client, 'get_people')

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_models
----------------------------------

Tests for `beckett.models` module.
"""

from beckett.models import BaseModel


def test_base_model_attributes():

    model = BaseModel(id='1')
    assert model.__str__() == '<Resource | 1>'

import unittest

import pytest
from app.model.relative import FEATURES, FamilyRelative
from app.service.helpers import arguments, connect_to_db
from app.service.relative_service import (relative_create, relative_delete,
                                          relative_load, relative_modify_attr,
                                          relative_save, relative_update,
                                          relatives_show)


def test_relative_create():
    db_connection = connect_to_db("../database/tree.db")
    db_cursor = db_connection.cursor()
    # move input loop ?
    relative_create(db_cursor)


def test_relative_save():
    pass


def test_relative_load():
    pass


def test_relative_select_all():
    pass


def test_relative_modify_attr():
    pass


def test_relative_find():
    pass


def test_relative_modify():
    pass


def test_relative_update():
    pass


def test_relative_delete():
    pass


def test_relative_show():
    pass

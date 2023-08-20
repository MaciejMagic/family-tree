import unittest

import pytest
from app.model.relative import FEATURES, FamilyRelative
from app.service.helpers import arguments, connect_to_db


def test_family_relative():
    person1 = FamilyRelative(first_name='Test_name1',
                             last_name='Test_last1',
                             gender='female',
                             date_of_birth='1950-09-09',
                             children=[100])
    person1._id = 101

    person2 = FamilyRelative(first_name='John',
                             second_name='Second',
                             last_name='Doe',
                             gender='male',
                             family_name='Doedoe',
                             date_of_birth='1970-12-12',
                             place_of_birth='Born_city',
                             date_of_death='2020-01-01',
                             place_of_death='Death_city',
                             mother=101,
                             father=102,
                             married=False,
                             spouse_current=103,
                             children=[103, 105],
                             phone='555-555-555',
                             email='john.doe@kmail.com',
                             events=['Event nr 1', 'Event nr 2'],
                             desc='Sample description')
    person2._id = 100

    assert person1.first_name == 'Test_name1'

    assert person2.last_name == 'Doe'
    assert person2.gender == 'male'
    assert person2.family_name == 'Doedoe'
    assert person2.date_of_birth == '1970-12-12'
    assert person2.place_of_birth == 'Born_city'
    assert person2.date_of_death == '2020-01-01'
    assert person2.place_of_death == 'Death_city'
    assert person2.children == [103, 105]
    assert person2.email == 'john.doe@kmail.com'
    assert person2.phone == '555-555-555'
    assert person2.events == ['Event nr 1', 'Event nr 2']
    assert person2.desc == 'Sample description'


def test_age():
    pass


def test_marry():
    pass

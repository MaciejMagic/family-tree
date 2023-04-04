# @dataclass ?

class Person():
    def __init__(self, first_name, last_name, gender, **kwargs):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.family_name = kwargs["family_name"]
        self.date_of_birth = kwargs["date_of_birth"]
        self.place_of_birth = kwargs["place_of_birth"]
        self.date_of_death = kwargs["date_of_death"]
        self.place_of_death = kwargs["place_of_death"]
        self.phone = kwargs["phone"]
        self.email = kwargs["email"]
        self.events = kwargs["events"]
        self.desc = kwargs["desc"]

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        if (first_name is None) or (14 < len(first_name) < 2):
            raise ValueError
        self._first_name = first_name

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        if (last_name is None) or (35 < len(last_name) < 2):
            raise ValueError
        self._last_name = last_name

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        self._gender = gender

    def __str__(self):
        return f"{self._first_name} {self._last_name}"

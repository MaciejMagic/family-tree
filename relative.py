from datetime import date
from validator_collection import validators, errors

# Note: make a @dataclass ?


class Person():
    """
    Main app class for data storage and
    transitions: database <-> graph generation input
    """

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

    # Properties

    @property
    def first_name(self):
        """ Returns objects first name """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        if (first_name is None) or (14 < len(first_name) < 2):
            raise ValueError
        self._first_name = first_name

    @property
    def last_name(self):
        """ Returns objects last name """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        if (last_name is None) or (35 < len(last_name) < 2):
            raise ValueError
        self._last_name = last_name

    @property
    def gender(self):
        """ Returns person gender """
        return self._gender

    @gender.setter
    def gender(self, gender):
        self._gender = gender

    @property
    def family_name(self):
        """ Returns objects family last name """
        return self._family_name

    @family_name.setter
    def family_name(self, family_name):
        if (family_name is None) or (35 < len(family_name) < 2):
            raise ValueError
        self._family_name = family_name

    @property
    def date_of_birth(self):
        """ Returns persons birthday """
        return repr(self._date_of_birth)

    @date_of_birth.setter
    def date_of_birth(self, date_of_birth):
        # Date input format must be in YYYY-MM-DD
        year, month, day = str(date_of_birth).split("-")
        self._date_of_birth = date(int(year), int(month), int(day))

    @property
    def date_of_death(self):
        """ Returns persons date of death """
        return repr(self._date_of_death)

    @date_of_death.setter
    def date_of_death(self, date_of_death):
        # Date input format must be in YYYY-MM-DD
        year, month, day = str(date_of_death).split("-")
        self._date_of_death = date(int(year), int(month), int(day))

    @property
    def phone(self):
        """ Returns persons phone number """
        return self._phone

    @phone.setter
    def phone(self, phone):
        self._phone = phone

    @property
    def email(self):
        """ Returns persons email address """
        return self._email

    @email.setter
    def email(self, email_address):
        try:
            if validators.email(email_address):
                self._email = email_address
            else:
                print("Invalid")
        except errors.EmptyValueError:
            print("Invalid")
        except errors.InvalidEmailError:
            print("Invalid")

    @property
    def events(self):
        """ Returns persons saved events as a long string """
        return self._events

    @events.setter
    def events(self, events):
        self._events = events

    @property
    def desc(self):
        """ Returns a persons description as a long string """
        return self._desc

    @desc.setter
    def desc(self, desc):
        self._desc = desc

    # Methods

    def __str__(self):
        return f"{self._first_name} {self._last_name}"

    def age(self) -> int:
        """
        Returns person age based on current date or years lived if deceased
        """
        if self._date_of_death is None:
            age_delta = date.today() - self._date_of_birth
        else:
            age_delta = self._date_of_death - self._date_of_birth

        return int(age_delta["years"])

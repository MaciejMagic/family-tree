from datetime import date

from validator_collection import checkers, errors, validators


class Person():
    """
    Main app class for data storage and
    transitions: database <-> graph generation input
    """

    def __init__(self, first_name, last_name, gender, **kwargs):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.family_name = kwargs.get("family_name")
        self.date_of_birth = kwargs.get("date_of_birth")
        self.place_of_birth = kwargs.get("place_of_birth")
        self.date_of_death = kwargs.get("date_of_death")
        self.place_of_death = kwargs.get("place_of_death")
        self.phone = kwargs.get("phone")
        self.email = kwargs.get("email")
        self._events = []
        self.events = kwargs.get("events")
        self._desc = []
        self.desc = kwargs.get("desc")

    # Properties

    @property
    def first_name(self) -> str:
        """ Returns objects first name """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name: str):
        if first_name.isalpha() is False:
            raise ValueError
        elif (first_name is None) or (14 < len(first_name) < 2):
            raise ValueError
        self._first_name = first_name

    @property
    def last_name(self) -> str:
        """ Returns objects last name """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name: str):
        if last_name.isalpha() is False:
            raise ValueError
        elif (last_name is None) or (35 < len(last_name) < 2):
            raise ValueError
        self._last_name = last_name

    @property
    def gender(self) -> str:
        """ Returns person gender """
        return self._gender

    @gender.setter
    def gender(self, gender: str):
        if gender.lower() not in ['female', 'male']:
            raise ValueError
        self._gender = gender

    @property
    def family_name(self) -> str:
        """ Returns objects family last name """
        return self._family_name

    @family_name.setter
    def family_name(self, family_name: str):
        # No alphabetic validation to allow regnal / family numbers
        if family_name:
            if (35 < len(family_name) < 2):
                raise ValueError
            self._family_name = family_name
        else:
            self._family_name = None

    @property
    def date_of_birth(self) -> str:
        """ Returns this persons birthday """
        return repr(self._date_of_birth)

    @date_of_birth.setter
    def date_of_birth(self, date_of_birth: str):
        # Date input must be in ISO 8601 format 'YYYY-MM-DD'
        if checkers.is_date(date_of_birth):
            year, month, day = str(date_of_birth).split("-")
            self._date_of_birth = date(int(year), int(month), int(day))
        else:
            raise ValueError("Invalid date format")

    @property
    def date_of_death(self) -> str:
        """ Returns this persons date of death """
        return repr(self._date_of_death)

    @date_of_death.setter
    def date_of_death(self, date_of_death: str):
        # Date input must be in ISO 8601 format 'YYYY-MM-DD'
        if checkers.is_date(date_of_death):
            year, month, day = str(date_of_death).split("-")
            self._date_of_death = date(int(year), int(month), int(day))
        else:
            raise ValueError("Invalid date format")

    @property
    def phone(self) -> str:
        """ Returns this persons phone number """
        return self._phone

    @phone.setter
    def phone(self, phone: str):
        # Check if inputed phone number string has at least 7 digits
        if (16 > len(filter(str.isdigit, phone)) > 6):
            self._phone = phone
        else:
            raise ValueError(
                "Phone value must be numerical and at least 7 digits long")

    @property
    def email(self) -> str:
        """ Returns this persons email address """
        return self._email

    @email.setter
    def email(self, email_address: str):
        try:
            if checkers.is_email(email_address):
                self._email = validators.email(email_address, allow_empty=True)
            else:
                raise ValueError("Invalid email value")
        except errors.InvalidEmailError as exc:
            raise errors.InvalidEmailError("Invalid email address") from exc

    @property
    def events(self) -> list[str]:
        """ Returns this persons saved events """
        return self._events

    @events.setter
    def events(self, event):
        self._events.append(event)

    @property
    def desc(self) -> list[str]:
        """ Returns this persons description """
        return self._desc

    @desc.setter
    def desc(self, desc):
        self._desc.append(desc)

    # Methods

    def __str__(self) -> str:
        if self._date_of_death is None:
            return f"{self._first_name} {self._last_name} ({self._date_of_birth} - )"
        else:
            name = (self._first_name + ' ' + self._last_name +
                    ', (' + self._date_of_birth + ' - ' + self._date_of_death + ')')
            return str(name)

    def age(self) -> int:
        """
        Returns person age based on current date or years lived if deceased
        """
        if self._date_of_death is None:
            age_delta = date.today() - self._date_of_birth
        else:
            age_delta = self._date_of_death - self._date_of_birth
        return int(age_delta["years"])

    def add_event(self, event: str) -> None:
        """ Add new event to persons bio """
        self._events.append(event)

    def add_desc(self, desc: str) -> None:
        """ Add new description to persons bio """
        self._desc.append(desc)

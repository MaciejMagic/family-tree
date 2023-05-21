from abc import ABC, abstractmethod
from datetime import date

from validator_collection import checkers, validators


class Person(ABC):
    """
    Abstract helper class for inheritance
    and method implementation enforcement
    """

    @abstractmethod
    def age(self) -> int:
        """
        Returns person age based on current date or years lived if deceased
        """
        raise NotImplementedError

    @abstractmethod
    def event_add(self, event: str) -> None:
        """ Add new event to persons bio """
        raise NotImplementedError

    @abstractmethod
    def desc_add(self, desc: str) -> None:
        """ Add new description to persons bio """
        raise NotImplementedError

    @abstractmethod
    def info(self):
        """ Prints all availible info about this person """
        raise NotImplementedError


class Relative(Person):
    """
    Main app class for data storage and
    transitions: database <-> graph generation input
    """

    def __init__(self, first_name: str, last_name: str, gender: str, **kwargs):
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
        self.id = kwargs.get("id")

    # Properties

    @property
    def first_name(self) -> str:
        """ Returns objects first name """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name: str) -> None:
        if first_name.isalpha() is False:
            raise ValueError("Error: numeric characters in first name")
        if first_name is None:
            raise ValueError("Error: first name value empty")
        if len(first_name) < 2:
            raise ValueError("Error: first name too short")
        if len(first_name) > 14:
            raise ValueError("Error: first name too long")
        self._first_name = first_name

    @property
    def last_name(self) -> str:
        """ Returns objects last name """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name: str) -> None:
        if last_name.isalpha() is False:
            raise ValueError("Error: numeric characters in last name")
        if last_name is None:
            raise ValueError("Error: last name value empty")
        if len(last_name) < 2:
            raise ValueError("Error: last name too short")
        if len(last_name) > 35:
            raise ValueError("Error: last name too long")
        self._last_name = last_name

    @property
    def gender(self) -> str:
        """ Returns person gender """
        return self._gender

    @gender.setter
    def gender(self, gender: str) -> None:
        if gender.strip().lower() not in ['female', 'male']:
            raise ValueError("Error: gender must be 'female' or 'male'")
        self._gender = gender

    @property
    def family_name(self) -> str | None:
        """ Returns objects family last name """
        return self._family_name

    @family_name.setter
    def family_name(self, family_name: str) -> None:
        # No alphabetic validation - to allow regnal / family numbers
        if family_name:
            if len(family_name) < 2:
                raise ValueError("Error: Family name too short")
            if len(family_name) > 35:
                raise ValueError("Error: Family name too long")
            self._family_name = family_name
        else:
            self._family_name = None

    @property
    def date_of_birth(self) -> str | None:
        """ Returns this persons birthday """
        return repr(self._date_of_birth)

    @date_of_birth.setter
    def date_of_birth(self, date_of_birth: str) -> None:
        # Date input must be in ISO 8601 format 'YYYY-MM-DD'
        if checkers.is_date(date_of_birth):
            year, month, day = str(date_of_birth).split("-")
            self._date_of_birth = date(int(year), int(month), int(day))
        else:
            self._date_of_birth = None
            raise ValueError(
                "Error: Invalid date format. Must be 'YYYY-MM-DD'")

    @property
    def place_of_birth(self) -> str | None:
        """ Returns this persons place of birth """
        return self._place_of_birth

    @place_of_birth.setter
    def place_of_birth(self, place_of_birth: str) -> None:
        if place_of_birth:
            if len(place_of_birth) < 2:
                raise ValueError("Error: city name too short")
            if len(place_of_birth) > 60:
                raise ValueError("Error: city name too long")
            self._place_of_birth = place_of_birth
        else:
            self._place_of_birth = None
            raise ValueError("Error: city name value empty")

    @property
    def date_of_death(self) -> str | None:
        """ Returns this persons date of death """
        return repr(self._date_of_death)

    @date_of_death.setter
    def date_of_death(self, date_of_death: str) -> None:
        # Date input must be in ISO 8601 format 'YYYY-MM-DD'
        if checkers.is_date(date_of_death):
            year, month, day = str(date_of_death).split("-")
            self._date_of_death = date(int(year), int(month), int(day))
        else:
            self._date_of_death = None
            raise ValueError(
                "Error: Invalid date format. Must be 'YYYY-MM-DD'")

    @property
    def place_of_death(self) -> str | None:
        """ Returns this persons place of death """
        return self._place_of_death

    @place_of_death.setter
    def place_of_death(self, place_of_death: str) -> None:
        if place_of_death:
            if len(place_of_death) < 2:
                raise ValueError("Error: city name too short")
            if len(place_of_death) > 60:
                raise ValueError("Error: city name too long")
            self._place_of_death = place_of_death
        else:
            self._place_of_death = None
            raise ValueError("Error: city name value empty")

    @property
    def phone(self) -> str | None:
        """ Returns this persons phone number """
        return self._phone

    @phone.setter
    def phone(self, phone: str) -> None:
        # Check if phone number string has at least 7 digits
        if (16 > len(filter(str.isdigit, phone)) > 6):
            self._phone = phone
        else:
            self._phone = None
            raise ValueError(
                "Error: Phone number must be numerical and min. 7 digits long")

    @property
    def email(self) -> str | None:
        """ Returns this persons email address """
        return self._email

    @email.setter
    def email(self, email_address: str) -> None:
        if email_address == "delete":
            self._email = None
        if checkers.is_email(email_address):
            self._email = validators.email(email_address, allow_empty=True)
        else:
            self._email = None
            raise ValueError("Invalid email address")

    @property
    def events(self) -> list[str]:
        """ Returns this persons saved events """
        if not self._events:
            print("Events are empty")
        else:
            return self._events

    @events.setter
    def events(self, event) -> None:
        self._events.append(event)

    @property
    def desc(self) -> list[str]:
        """ Returns this persons description """
        if not self._desc:
            print("Description is empty")
        else:
            return self._desc

    @desc.setter
    def desc(self, desc) -> None:
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

    def event_add(self, event: str) -> None:
        """ Add new event to persons bio """
        self._events.append(event)

    def desc_add(self, desc: str) -> None:
        """ Add new description to persons bio """
        self._desc.append(desc)

    def info(self) -> str:
        """
        Returns all availible info about this person in a multiline string
        """

        properties = [attribute for attribute in dir(self) if not attribute.startswith(
            '_') and not callable(getattr(self, attribute))]

        summary = ""

        for prop in properties:
            if getattr(self, prop):
                summary += (f"{prop}: {getattr(self, prop)}" + "\n")

        return summary

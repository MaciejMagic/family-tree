from datetime import date, timedelta

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
        # Create a setter for datetime format compliance
        self.date_of_birth = kwargs["date_of_birth"]
        self.place_of_birth = kwargs["place_of_birth"]
        # Create a setter for datetime format compliance
        self.date_of_death = kwargs["date_of_death"]
        self.place_of_death = kwargs["place_of_death"]
        self.phone = kwargs["phone"]
        # Create a setter for email format compliance (with regex?)
        self.email = kwargs["email"]
        self.events = kwargs["events"]
        self.desc = kwargs["desc"]

    # Properties

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

    # Methods

    def __str__(self):
        return f"{self._first_name} {self._last_name}"

    def age(self) -> int:
        """
        Returns person age based on current date or if deceased years lived
        """
        # TO DO - if deceased then (not from timedelta)

        # Substraction of dates equals to a timedelta object
        age_delta = date.today() - self.date_of_birth
        age_years = age_delta["years"]

        return int(age_years)

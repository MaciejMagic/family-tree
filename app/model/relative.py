import sys
from datetime import date

from model.person import FamilyData, Person, PersonData
from validator_collection import checkers, validators

FEATURES = ("first_name",
            "second_name",
            "last_name",
            "gender",
            "family_name",
            "date_of_birth",
            "place_of_birth",
            "date_of_death",
            "place_of_death",
            "mother",
            "father",
            "married",
            "spouse_current",
            "children",
            "phone",
            "email",
            "events",
            "desc")


class FamilyRelative(Person):
    """
    Main app class for people objects.
    Data storage and transitions: database <-> graph generation.
    """

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self._id: int = None
        self.person_data: PersonData = PersonData(
            second_name=kwargs.get("second_name"),
            phone=kwargs.get("phone"),
            email=kwargs.get("email"),
            events=kwargs.get("events"),
            desc=kwargs.get("desc")
        )
        self.family_data: FamilyData = FamilyData(
            family_name=kwargs.get("family_name"),
            mother=kwargs.get("mother"),
            father=kwargs.get("father"),
            spouse_current=kwargs.get("spouse_current"),
            children=kwargs.get("children"),
            married=kwargs.get("married")
        )

        self.generation: int = 0
        self.cluster: int = 0

    def __str__(self) -> str:
        if self._date_of_death is None:
            return f"{self._first_name} {self._last_name} ({self._date_of_birth} - )"

        name = (self._first_name + ' ' + self._last_name +
                ', (' + self._date_of_birth + ' - ' + self._date_of_death + ')')
        return str(name)

    # Properties

    @property
    def first_name(self) -> str:
        """ Returns objects first name """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name: str) -> None:
        if first_name.isalpha() is False:
            raise ValueError(
                "Error > Assigning first name > Numeric characters in first name")
        if first_name is None:
            self._first_name = "<missing>"
        if len(first_name) < 2:
            raise ValueError(
                "Error > Assigning first name > First name too short")
        if len(first_name) > 14:
            raise ValueError(
                "Error > Assigning first name > First name too long")
        self._first_name = first_name

    @property
    def last_name(self) -> str:
        """ Returns objects last name """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name: str) -> None:
        if last_name.isalpha() is False:
            raise ValueError(
                "Error > Assigning last name > Numeric characters in last name")
        if last_name is None:
            self._last_name = "<missing>"
        if len(last_name) < 2:
            raise ValueError(
                "Error > Assigning last name > Last name too short")
        if len(last_name) > 35:
            raise ValueError(
                "Error > Assigning last name > Last name too long")
        self._last_name = last_name

    @property
    def gender(self) -> str:
        """ Returns person gender """
        return self._gender

    @gender.setter
    def gender(self, gender: str) -> None:
        if gender.strip().lower() not in ['female', 'male']:
            raise ValueError(
                "Error > Assigning gender > Gender must be 'female' or 'male'")
        self._gender = gender

    @property
    def family_name(self) -> str | None:
        """ Returns objects family last name """
        return self.family_data.family_name

    @family_name.setter
    def family_name(self, family_name: str) -> None:
        # No alphabetic validation - to allow regnal / family numbers
        if family_name:
            if len(family_name) < 2:
                raise ValueError(
                    "Error > Assigning family name > Family name too short")
            if len(family_name) > 35:
                raise ValueError(
                    "Error > Assigning family name > Family name too long")
            self.family_data.family_name = family_name
        else:
            self.family_data.family_name = None

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
                "Error > Assigning Date of Birth > Invalid date format (Must be 'YYYY-MM-DD')")

    @property
    def place_of_birth(self) -> str | None:
        """ Returns this persons place of birth """
        return self._place_of_birth

    @place_of_birth.setter
    def place_of_birth(self, place_of_birth: str) -> None:
        if place_of_birth:
            if len(place_of_birth) < 2:
                raise ValueError(
                    "Error > Assigning place of birth > City name too short")
            if len(place_of_birth) > 60:
                raise ValueError(
                    "Error > Assigning place of birth > City name too long")
            self._place_of_birth = place_of_birth
        else:
            self._place_of_birth = None
            raise ValueError(
                "Error > Assigning place of birth > City name value empty")

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
                "Error > Assigning date of death > Invalid date format (Must be 'YYYY-MM-DD')")

    @property
    def place_of_death(self) -> str | None:
        """ Returns this persons place of death """
        return self._place_of_death

    @place_of_death.setter
    def place_of_death(self, place_of_death: str) -> None:
        if place_of_death:
            if len(place_of_death) < 2:
                raise ValueError(
                    "Error > Assigning place of death > City name too short")
            if len(place_of_death) > 60:
                raise ValueError(
                    "Error > Assigning place of death > City name too long")
            self._place_of_death = place_of_death
        else:
            self._place_of_death = None
            raise ValueError(
                "Error > Assigning place of death > City name value empty")

    @property
    def phone(self) -> str | None:
        """ Returns this persons phone number """
        return self.person_data.phone

    @phone.setter
    def phone(self, phone: str) -> None:
        # Check if phone number string has at least 7 digits
        if len(filter(str.isdigit, phone)) > 6 and len(filter(str.isdigit, phone)) < 16:
            self.person_data.phone = phone
        else:
            self.person_data.phone = None
            raise ValueError(
                "Error > Assigning phone number > Must be numerical value and min. 7 digits long")

    @property
    def email(self) -> str | None:
        """ Returns this persons email address """
        return self.person_data.email

    @email.setter
    def email(self, email_address: str) -> None:
        if email_address == "delete":
            self.person_data.email = None
        if checkers.is_email(email_address):
            self.person_data.email = validators.email(
                email_address, allow_empty=True)
        else:
            self.person_data.email = None
            raise ValueError("Error > Assigning email > Invalid address")

    @property
    def events(self) -> list[str] | None:
        """ Returns this persons saved events """
        if not self.person_data.events:
            print("Event list is empty")
            return None
        return self.person_data.events

    @events.setter
    def events(self, event) -> None:
        self.person_data.events.append(event)

    @property
    def desc(self) -> list[str] | None:
        """ Returns this persons description """
        if not self.person_data.desc:
            print("Description is empty")
            return None
        return self.person_data.desc

    @desc.setter
    def desc(self, desc) -> None:
        self.person_data.desc.append(desc)

    @property
    def children(self) -> list[int] | None:
        """ Returns this persons children list """
        return self.family_data.children

    @children.setter
    def children(self, children: int | list[int]) -> None:
        self.family_data.children.append(children)

    # Methods

    def age(self) -> int:
        """
        Returns person age based on current date or years lived if deceased
        """
        if self._date_of_death is None:
            age_delta = date.today() - self._date_of_birth
        else:
            age_delta = self._date_of_death - self._date_of_birth
        return int(age_delta["years"])

    def info(self) -> str:
        """
        Returns all availible info about this person in a multiline string
        """
        properties = [attribute for attribute in dir(self) if not attribute.startswith(
            '_') and not callable(getattr(self, attribute))]

        summary = """\n"""

        for feature_main in FEATURES:
            for feature_instance in properties:
                if (feature_main == feature_instance) and getattr(self, feature_instance):
                    summary += (f"{feature_instance}: {getattr(self, feature_instance)}" + "\n")
        return summary

    def event_add(self, event: str) -> None:
        """ Add new event to persons bio """
        self.person_data.events.append(event)

    def desc_add(self, desc: str) -> None:
        """ Add new description to persons bio """
        self.person_data.desc.append(desc)

    def marry(self, status: bool = True) -> None:
        """ Change married status for this person """
        if self.family_data.married is True:
            print("Error > Status not changed > Already married", file=sys.stderr)
        self.family_data.married = status

    def set_mother(self, mother_id) -> None:
        """ Sets mother relative for this person """
        if int(mother_id):
            self.family_data.mother = mother_id
        else:
            raise ValueError("Error > Assigning mother id > Not an integer")

    def set_father(self, father_id) -> None:
        """ Sets father relative for this person """
        if int(father_id):
            self.family_data.father = father_id
        else:
            raise ValueError("Error > Assigning father id > Not an integer")

    def set_spouse(self, spouse) -> None:
        """ Sets spouse relative for this person """
        if int(spouse):
            self.family_data.spouse_current = spouse
        else:
            raise ValueError("Error > Assigning spouse id > Not an integer")

    def child_add(self, child) -> None:
        """ Adds a child to Persons list of children """
        if int(child):
            self.family_data.children.append(child)
        else:
            raise ValueError("Error > Adding child > Invalid value")
